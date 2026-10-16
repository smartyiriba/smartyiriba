from decimal import Decimal
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User
from apps.catalog.models import Category, Service
from apps.quotes.models import QuoteRequest
from .models import Order, OrderLine, Invoice, Payment, AuditEvent
from .services import convert_quote, issue_invoice, confirm_payment

class CommerceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='test-password')
        cls.customer = User.objects.create_user(username='client', email='client@example.com', address='Bamako')
        cls.other = User.objects.create_user(username='autre')
        category = Category.objects.create(name='Web', slug='web')
        cls.service = Service.objects.create(category=category, title='Site', slug='site', active=True)

    def order(self, currency='XOF'):
        order = Order.objects.create(customer=self.customer, currency=currency)
        OrderLine.objects.create(order=order, description='Site professionnel', quantity=2, unit_price=Decimal('1000'), discount=Decimal('100'), tax_rate=Decimal('18'))
        return order

    def invoice(self):
        return issue_invoice(self.order().pk, self.admin, 'Paiement à réception')

    def test_totals_and_immutable_invoice_snapshot(self):
        order = self.order()
        invoice = issue_invoice(order.pk, self.admin, 'Paiement à réception')
        self.assertEqual(invoice.total, Decimal('2242'))
        self.assertEqual(invoice.items[0]['subtotal'], '1900')
        self.assertEqual(invoice.items[0]['tax'], '342')
        self.customer.address = 'Autre adresse'
        self.customer.save()
        invoice.refresh_from_db()
        self.assertEqual(invoice.customer_address, 'Bamako')
        self.assertEqual(issue_invoice(order.pk, self.admin, 'Autre texte').pk, invoice.pk)
        self.assertEqual(AuditEvent.objects.filter(action='invoice.issued').count(), 1)
        line = order.lines.get()
        order.refresh_from_db()
        line.order = order
        with self.assertRaises(ValidationError): line.full_clean()

    def test_rounding_uses_currency_precision(self):
        order = self.order('EUR')
        line = order.lines.get()
        line.unit_price = Decimal('10.01')
        line.discount = Decimal('0.01')
        line.tax_rate = Decimal('5.50')
        line.save()
        self.assertEqual(issue_invoice(order.pk, self.admin, 'À réception').total, Decimal('21.11'))

    def test_partial_and_complete_payments_are_idempotent(self):
        invoice = self.invoice()
        first = Payment.objects.create(invoice=invoice, reference='RECU-1', amount=1000, method='cash')
        confirm_payment(first.pk, self.admin)
        confirm_payment(first.pk, self.admin)
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, 'partial')
        self.assertEqual(invoice.balance, Decimal('1242'))
        second = Payment.objects.create(invoice=invoice, reference='RECU-2', amount=1242, method='bank')
        confirm_payment(second.pk, self.admin)
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, 'paid')
        self.assertEqual(invoice.balance, 0)
        self.assertEqual(AuditEvent.objects.filter(action='payment.confirmed').count(), 2)

    def test_overpayment_rolls_back(self):
        invoice = self.invoice()
        payment = Payment.objects.create(invoice=invoice, reference='OVER', amount=3000, method='cash')
        with self.assertRaises(ValidationError): confirm_payment(payment.pk, self.admin)
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'pending')
        self.assertFalse(AuditEvent.objects.filter(action='payment.confirmed').exists())

    def test_permissions(self):
        order = self.order()
        with self.assertRaises(PermissionDenied): issue_invoice(order.pk, self.customer, 'À réception')
        invoice = issue_invoice(order.pk, self.admin, 'À réception')
        payment = Payment.objects.create(invoice=invoice, reference='DENIED', amount=1000, method='cash')
        with self.assertRaises(PermissionDenied): confirm_payment(payment.pk, self.customer)

    def test_quote_conversion_is_unique_and_does_not_invent_price(self):
        quote = QuoteRequest.objects.create(customer=self.customer, service=self.service, name='Client', email='client@example.com', phone='123', country='Mali', customer_type='individual', description='Site', status='accepted')
        order = convert_quote(quote.pk, self.admin)
        self.assertEqual(convert_quote(quote.pk, self.admin).pk, order.pk)
        self.assertEqual(order.lines.count(), 0)
        with self.assertRaises(ValidationError): issue_invoice(order.pk, self.admin, 'À réception')
        quote.refresh_from_db()
        self.assertEqual(quote.status, 'converted')

    def test_client_cannot_access_another_invoice(self):
        invoice = self.invoice()
        url = reverse('invoice_detail', args=[invoice.number])
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertNotContains(self.client.get(reverse('orders')), invoice.order.number)
        self.client.force_login(self.customer)
        self.assertContains(self.client.get(url), invoice.number)
        self.assertContains(self.client.get(reverse('orders')), invoice.order.number)

    def test_invalid_discount_rejected_by_database(self):
        order = self.order()
        with self.assertRaises(IntegrityError), transaction.atomic():
            OrderLine.objects.create(order=order, description='Invalide', quantity=1, unit_price=100, discount=200)

    def test_fractional_xof_payment_rejected(self):
        invoice = self.invoice()
        payment = Payment.objects.create(invoice=invoice, reference='FRACTION', amount=Decimal('1.50'), method='cash')
        with self.assertRaises(ValidationError): confirm_payment(payment.pk, self.admin)

    def test_sensitive_records_are_readonly_in_admin(self):
        invoice = self.invoice()
        self.client.force_login(self.admin)
        response = self.client.post(reverse('admin:commerce_invoice_change', args=[invoice.pk]), {'total': '1', 'status': 'paid'})
        self.assertEqual(response.status_code, 403)
        invoice.refresh_from_db()
        self.assertEqual(invoice.total, 2242)
        self.assertEqual(invoice.status, 'issued')

    def test_admin_order_and_payment_forms_render(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('admin:commerce_order_add')).status_code, 200)
        order = self.order()
        self.assertEqual(self.client.get(reverse('admin:commerce_order_change', args=[order.pk])).status_code, 200)
        invoice = issue_invoice(order.pk, self.admin, 'À réception')
        self.assertEqual(self.client.get(reverse('admin:commerce_invoice_change', args=[invoice.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('admin:commerce_payment_add')).status_code, 200)

    def test_pdf_download_is_private_and_contains_snapshot(self):
        from io import BytesIO
        from pypdf import PdfReader
        invoice = self.invoice()
        url = reverse('invoice_download', args=[invoice.number])
        self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_login(self.customer)
        response = self.client.get(url)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertEqual(response['Cache-Control'], 'private, no-store')
        text = ''.join(page.extract_text() for page in PdfReader(BytesIO(response.content)).pages)
        self.assertIn(invoice.number, text)
        self.assertIn('2242', text)
        self.assertIn('Site professionnel', text)

    def test_partial_full_refund_and_idempotency(self):
        from .models import Refund
        from .services import confirm_refund
        invoice = self.invoice()
        payment = Payment.objects.create(invoice=invoice, reference='PAY-REFUND', amount=invoice.total, method='cash')
        confirm_payment(payment.pk, self.admin)
        refund = Refund.objects.create(payment=payment, reference='REF-1', amount=1000, reason='Prestation réduite')
        with self.assertRaises(PermissionDenied): confirm_refund(refund.pk, self.customer)
        confirm_refund(refund.pk, self.admin)
        confirm_refund(refund.pk, self.admin)
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, 'partially_refunded')
        self.assertEqual(invoice.net_received, 1242)
        second = Refund.objects.create(payment=payment, reference='REF-2', amount=1242, reason='Annulation du solde')
        confirm_refund(second.pk, self.admin)
        invoice.refresh_from_db()
        invoice.order.refresh_from_db()
        self.assertEqual(invoice.status, 'refunded')
        self.assertEqual(invoice.order.status, 'refunded')
        self.assertEqual(invoice.net_received, 0)
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'confirmed')
        self.assertEqual(AuditEvent.objects.filter(action='refund.confirmed').count(), 2)

    def test_refund_cannot_exceed_payment_or_use_wrong_precision(self):
        from .models import Refund
        from .services import confirm_refund
        invoice = self.invoice()
        payment = Payment.objects.create(invoice=invoice, reference='PAY-EXCESS', amount=invoice.total, method='cash')
        confirm_payment(payment.pk, self.admin)
        for reference, amount in [('TOO-MUCH', '2243'), ('CENTS', '0.50')]:
            refund = Refund.objects.create(payment=payment, reference=reference, amount=amount, reason='Test')
            with self.assertRaises(ValidationError): confirm_refund(refund.pk, self.admin)
            refund.refresh_from_db()
            self.assertEqual(refund.status, 'pending')
        self.assertFalse(AuditEvent.objects.filter(action='refund.confirmed').exists())

    def test_cancel_unpaid_invoice_and_pending_payment(self):
        from .services import cancel_order
        invoice = self.invoice()
        payment = Payment.objects.create(invoice=invoice, reference='PAY-CANCEL', amount=100, method='cash')
        with self.assertRaises(PermissionDenied): cancel_order(invoice.order_id, self.customer, 'Test')
        with self.assertRaises(ValidationError): cancel_order(invoice.order_id, self.admin, '')
        cancel_order(invoice.order_id, self.admin, 'Demande du client')
        cancel_order(invoice.order_id, self.admin, 'Demande répétée')
        invoice.refresh_from_db()
        payment.refresh_from_db()
        self.assertEqual(invoice.status, 'cancelled')
        self.assertEqual(payment.status, 'cancelled')
        with self.assertRaises(ValidationError): confirm_payment(payment.pk, self.admin)
        self.assertEqual(AuditEvent.objects.filter(action='order.cancelled').count(), 1)

    def test_paid_invoice_cannot_be_cancelled(self):
        from .services import cancel_order
        invoice = self.invoice()
        payment = Payment.objects.create(invoice=invoice, reference='PAY-KEEP', amount=100, method='cash')
        confirm_payment(payment.pk, self.admin)
        with self.assertRaises(ValidationError): cancel_order(invoice.order_id, self.admin, 'Test')
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, 'partial')

    def test_issuer_is_snapshotted_and_refund_admin_renders(self):
        from .models import Refund
        with self.settings(BUSINESS_ISSUER={'name': 'Émetteur test', 'address': 'Adresse test'}):
            invoice = self.invoice()
        self.assertEqual(invoice.issuer['name'], 'Émetteur test')
        payment = Payment.objects.create(invoice=invoice, reference='PAY-ADMIN', amount=invoice.total, method='cash')
        confirm_payment(payment.pk, self.admin)
        refund = Refund.objects.create(payment=payment, reference='REF-ADMIN', amount=10, reason='Test')
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse('admin:commerce_refund_add')).status_code, 200)
        self.assertEqual(self.client.get(reverse('admin:commerce_refund_change', args=[refund.pk])).status_code, 200)
