from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from apps.quotes.models import QuoteRequest
from .models import Order, OrderLine, Invoice, Payment, AuditEvent, Refund, money

def require(actor, permission):
    if not actor.is_active or not actor.has_perm('commerce.' + permission):
        raise PermissionDenied

def audit(actor, action, target, before, after):
    AuditEvent.objects.create(actor=actor, action=action, target=str(target), before=before, after=after)

@transaction.atomic
def convert_quote(quote_id, actor):
    require(actor, 'add_order')
    quote = QuoteRequest.objects.select_for_update().select_related('service').get(pk=quote_id)
    existing = Order.objects.filter(quote=quote).first()
    if existing:
        return existing
    if quote.status != QuoteRequest.Status.ACCEPTED or not quote.customer_id:
        raise ValidationError('Le devis doit être accepté et rattaché à un compte client.')
    order = Order.objects.create(customer=quote.customer, quote=quote, currency=quote.service.currency)
    # La demande ne contient pas encore une offre chiffrée acceptée : ne pas inventer son prix.
    quote.status = QuoteRequest.Status.CONVERTED
    quote.save(update_fields=['status'])
    audit(actor, 'quote.converted', order.number, {'quote': str(quote.reference), 'status': 'accepted'}, {'status': 'converted'})
    return order

@transaction.atomic
def issue_invoice(order_id, actor, payment_terms):
    require(actor, 'add_invoice')
    order = Order.objects.select_for_update().select_related('customer').get(pk=order_id)
    existing = Invoice.objects.filter(order=order).first()
    if existing:
        return existing
    if order.status != Order.Status.DRAFT:
        raise ValidationError('Seule une commande brouillon peut être facturée dans ce premier lot.')
    lines = list(order.lines.select_related('order'))
    if not lines or not payment_terms.strip():
        raise ValidationError('Ajoutez au moins une ligne et les modalités de paiement.')
    for line in lines:
        line.full_clean()
        if money(line.unit_price, order.currency) != line.unit_price or money(line.discount, order.currency) != line.discount:
            raise ValidationError('Les prix et remises doivent respecter la précision de la devise.')
    items = [{'description': line.description, 'quantity': line.quantity, 'unit_price': str(line.unit_price), 'discount': str(line.discount), 'tax_rate': str(line.tax_rate), 'subtotal': str(line.subtotal), 'tax': str(line.tax), 'total': str(line.total)} for line in lines]
    customer = order.customer
    invoice = Invoice.objects.create(order=order, customer_name=customer.organization or customer.get_full_name() or customer.username, customer_address=customer.address, customer_email=customer.email, currency=order.currency, items=items, total=sum(line.total for line in lines), issuer=dict(getattr(settings, 'BUSINESS_ISSUER', {})), payment_terms=payment_terms, status=Invoice.Status.PAID if sum(line.total for line in lines) == 0 else Invoice.Status.ISSUED)
    order.status = Order.Status.CONFIRMED
    order.save(update_fields=['status'])
    audit(actor, 'invoice.issued', invoice.number, {'order_status': 'draft'}, {'order_status': 'confirmed', 'total': str(invoice.total), 'currency': invoice.currency})
    return invoice

@transaction.atomic
def confirm_payment(payment_id, actor):
    require(actor, 'confirm_payment')
    # Toujours verrouiller la facture avant le paiement pour sérialiser les règlements concurrents.
    invoice_id = Payment.objects.values_list('invoice_id', flat=True).get(pk=payment_id)
    invoice = Invoice.objects.select_for_update().get(pk=invoice_id)
    payment = Payment.objects.select_for_update().get(pk=payment_id)
    if payment.status == Payment.Status.CONFIRMED:
        return payment
    if payment.status != Payment.Status.PENDING or invoice.status in (Invoice.Status.CANCELLED, Invoice.Status.PARTIALLY_REFUNDED, Invoice.Status.REFUNDED):
        raise ValidationError('Ce paiement ne peut pas être confirmé.')
    payment.full_clean()
    if payment.amount > invoice.balance:
        raise ValidationError('Le paiement dépasse le solde restant.')
    payment.status = Payment.Status.CONFIRMED
    payment.confirmed_by = actor
    payment.confirmed_at = timezone.now()
    payment.save(update_fields=['status', 'confirmed_by', 'confirmed_at'])
    previous = invoice.status
    invoice.status = Invoice.Status.PAID if invoice.balance == 0 else Invoice.Status.PARTIAL
    invoice.save(update_fields=['status'])
    audit(actor, 'payment.confirmed', payment.reference, {'payment_status': 'pending', 'invoice_status': previous}, {'payment_status': 'confirmed', 'invoice_status': invoice.status, 'amount': str(payment.amount), 'currency': invoice.currency})
    return payment

@transaction.atomic
def cancel_order(order_id, actor, reason):
    require(actor, 'cancel_order')
    if not reason.strip():
        raise ValidationError('Le motif est obligatoire.')
    order = Order.objects.select_for_update().get(pk=order_id)
    if order.status == Order.Status.CANCELLED:
        return order
    if order.status not in (Order.Status.DRAFT, Order.Status.CONFIRMED):
        raise ValidationError('Cette commande ne peut pas être annulée.')
    invoice = Invoice.objects.select_for_update().filter(order=order).first()
    if invoice:
        if invoice.paid_amount:
            raise ValidationError('Une commande encaissée nécessite un remboursement, pas une annulation simple.')
        invoice.status = Invoice.Status.CANCELLED
        invoice.save(update_fields=['status'])
        invoice.payments.filter(status=Payment.Status.PENDING).update(status=Payment.Status.CANCELLED)
    previous = order.status
    order.status = Order.Status.CANCELLED
    order.save(update_fields=['status'])
    audit(actor, 'order.cancelled', order.number, {'status': previous}, {'status': order.status, 'reason': reason})
    return order

@transaction.atomic
def confirm_refund(refund_id, actor):
    require(actor, 'confirm_refund')
    info = Refund.objects.values('payment__invoice__order_id', 'payment__invoice_id', 'payment_id').get(pk=refund_id)
    order = Order.objects.select_for_update().get(pk=info['payment__invoice__order_id'])
    invoice = Invoice.objects.select_for_update().get(pk=info['payment__invoice_id'])
    payment = Payment.objects.select_for_update().get(pk=info['payment_id'])
    refund = Refund.objects.select_for_update().get(pk=refund_id)
    if refund.status == Refund.Status.CONFIRMED:
        return refund
    refund.full_clean()
    # Ce lot limite les remboursements aux factures intégralement réglées.
    if invoice.balance != 0 or invoice.status == Invoice.Status.CANCELLED:
        raise ValidationError('Le remboursement nécessite une facture intégralement réglée.')
    refunded = payment.refunds.filter(status=Refund.Status.CONFIRMED).aggregate(amount=Sum('amount'))['amount'] or 0
    if refund.amount > payment.amount - refunded:
        raise ValidationError('Le remboursement dépasse le montant encore remboursable du paiement.')
    refund.status = Refund.Status.CONFIRMED
    refund.confirmed_by = actor
    refund.confirmed_at = timezone.now()
    refund.save(update_fields=['status', 'confirmed_by', 'confirmed_at'])
    previous = invoice.status
    invoice.status = Invoice.Status.REFUNDED if invoice.refunded_amount == invoice.total else Invoice.Status.PARTIALLY_REFUNDED
    invoice.save(update_fields=['status'])
    if invoice.status == Invoice.Status.REFUNDED:
        order.status = Order.Status.REFUNDED
        order.save(update_fields=['status'])
    audit(actor, 'refund.confirmed', refund.reference, {'status': 'pending', 'invoice_status': previous}, {'status': 'confirmed', 'invoice_status': invoice.status, 'amount': str(refund.amount), 'reason': refund.reason})
    return refund
