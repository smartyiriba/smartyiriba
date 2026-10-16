import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Sum

def reference(prefix):
    return prefix + '-' + uuid.uuid4().hex.upper()
def order_number(): return reference('CMD')
def invoice_number(): return reference('FAC')
def money(value, currency):
    return Decimal(value).quantize(Decimal('1') if currency == 'XOF' else Decimal('0.01'), rounding=ROUND_HALF_UP)

class Order(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Brouillon'
        PENDING = 'pending', 'En attente'
        CONFIRMED = 'confirmed', 'Confirmée'
        PREPARING = 'preparing', 'En préparation'
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Terminée'
        CANCELLED = 'cancelled', 'Annulée'
        REFUNDED = 'refunded', 'Remboursée'
    number = models.CharField(max_length=40, unique=True, default=order_number, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    quote = models.OneToOneField('quotes.QuoteRequest', on_delete=models.PROTECT, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=[('XOF', 'FCFA'), ('EUR', 'EUR'), ('USD', 'USD')], default='XOF')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
        permissions = [('cancel_order', 'Peut annuler une commande sans encaissement')]
    def __str__(self): return self.number
    @property
    def total(self): return sum((line.total for line in self.lines.all()), Decimal('0')) if self.pk else Decimal('0')

class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lines')
    description = models.CharField(max_length=250)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text='Remise totale sur cette ligne, avant taxe.')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(quantity__gt=0), name='line_positive_quantity'),
            models.CheckConstraint(condition=Q(unit_price__gte=0), name='line_positive_price'),
            models.CheckConstraint(condition=Q(discount__gte=0) & Q(discount__lte=models.F('unit_price') * models.F('quantity')), name='line_valid_discount'),
            models.CheckConstraint(condition=Q(tax_rate__gte=0) & Q(tax_rate__lte=100), name='line_valid_tax'),
        ]
    def clean(self):
        super().clean()
        if self.order_id and self.order.status != Order.Status.DRAFT:
            raise ValidationError('Les lignes sont figées après confirmation.')
        if self.quantity and self.unit_price is not None and self.discount is not None and self.discount > self.quantity * self.unit_price:
            raise ValidationError('La remise dépasse le montant de la ligne.')
    @property
    def subtotal(self): return money(self.unit_price * self.quantity - self.discount, self.order.currency)
    @property
    def tax(self): return money(self.subtotal * self.tax_rate / Decimal('100'), self.order.currency)
    @property
    def total(self): return self.subtotal + self.tax

class Invoice(models.Model):
    class Status(models.TextChoices):
        ISSUED = 'issued', 'Émise'
        PARTIAL = 'partial', 'Partiellement payée'
        PAID = 'paid', 'Payée'
        CANCELLED = 'cancelled', 'Annulée'
        PARTIALLY_REFUNDED = 'partially_refunded', 'Partiellement remboursée'
        REFUNDED = 'refunded', 'Remboursée'
    issuer = models.JSONField(default=dict, blank=True)
    number = models.CharField(max_length=40, unique=True, default=invoice_number, editable=False)
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='invoice')
    customer_name = models.CharField(max_length=250)
    customer_address = models.TextField(blank=True)
    customer_email = models.EmailField()
    currency = models.CharField(max_length=3)
    items = models.JSONField(default=list)
    total = models.DecimalField(max_digits=14, decimal_places=2)
    payment_terms = models.TextField()
    issued_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ISSUED)
    class Meta:
        ordering = ['-issued_at']
        constraints = [models.CheckConstraint(condition=Q(total__gte=0), name='invoice_positive_total')]
    def __str__(self): return self.number
    @property
    def paid_amount(self):
        return self.payments.filter(status=Payment.Status.CONFIRMED).aggregate(amount=Sum('amount'))['amount'] or Decimal('0')
    @property
    def balance(self): return self.total - self.paid_amount
    @property
    def refunded_amount(self):
        return Refund.objects.filter(payment__invoice=self, status=Refund.Status.CONFIRMED).aggregate(amount=Sum('amount'))['amount'] or Decimal('0')
    @property
    def net_received(self): return self.paid_amount - self.refunded_amount


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        CONFIRMED = 'confirmed', 'Confirmé'
        FAILED = 'failed', 'Échoué'
        CANCELLED = 'cancelled', 'Annulé'
    class Method(models.TextChoices):
        MOBILE = 'mobile', 'Paiement mobile'
        BANK = 'bank', 'Virement bancaire'
        CASH = 'cash', 'Espèces'
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='payments')
    reference = models.CharField(max_length=160, unique=True, help_text='Référence unique du règlement ou du reçu.')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    method = models.CharField(max_length=12, choices=Method.choices)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    confirmed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='confirmed_payments')
    class Meta:
        permissions = [('confirm_payment', 'Peut confirmer un paiement manuel')]
        constraints = [models.CheckConstraint(condition=Q(amount__gt=0), name='payment_positive_amount')]
    def __str__(self): return self.reference
    def clean(self):
        super().clean()
        if self.invoice_id and self.amount is not None:
            if money(self.amount, self.invoice.currency) != self.amount:
                raise ValidationError('Le montant doit respecter la précision de la devise de la facture.')
            if self.invoice.status == Invoice.Status.CANCELLED:
                raise ValidationError('Cette facture est annulée.')

class AuditEvent(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    action = models.CharField(max_length=80)
    target = models.CharField(max_length=160)
    before = models.JSONField(default=dict)
    after = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

class Refund(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        CONFIRMED = 'confirmed', 'Confirmé'
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name='refunds')
    reference = models.CharField(max_length=160, unique=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    confirmed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='confirmed_refunds')
    class Meta:
        permissions = [('confirm_refund', 'Peut confirmer un remboursement manuel')]
        constraints = [models.CheckConstraint(condition=Q(amount__gt=0), name='refund_positive_amount')]
    def __str__(self): return self.reference
    def clean(self):
        super().clean()
        if not self.reason.strip():
            raise ValidationError('Le motif est obligatoire.')
        if self.payment_id:
            if self.payment.status != Payment.Status.CONFIRMED:
                raise ValidationError('Seul un paiement confirmé peut être remboursé.')
            if self.amount is not None and money(self.amount, self.payment.invoice.currency) != self.amount:
                raise ValidationError('Le remboursement doit respecter la précision de la devise.')
