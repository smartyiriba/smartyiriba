from django.contrib import admin, messages
from django import forms
from django.contrib.admin.helpers import ActionForm
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Order, OrderLine, Invoice, Payment, AuditEvent, Refund
from .services import issue_invoice, confirm_payment, cancel_order, confirm_refund

class CancellationActionForm(ActionForm):
    reason = forms.CharField(label="Motif de l'annulation", required=False)

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1
    def has_add_permission(self, request, obj=None):
        return super().has_add_permission(request, obj) and (obj is None or obj.status == 'draft')
    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and (obj is None or obj.status == 'draft')
    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and (obj is None or obj.status == 'draft')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        with transaction.atomic():
            if request.method == 'POST' and object_id:
                Order.objects.select_for_update().filter(pk=object_id).first()
            return super().changeform_view(request, object_id, form_url, extra_context)

    list_display = ('number', 'customer', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency')
    search_fields = ('number', 'customer__username')
    inlines = [OrderLineInline]
    action_form = CancellationActionForm
    actions = ['issue', 'cancel_selected']
    readonly_fields = ('number', 'status', 'created_at', 'total', 'quote')
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + (('customer', 'currency') if obj and obj.status != 'draft' else ())
    def has_delete_permission(self, request, obj=None):
        return False
    @admin.action(description='Émettre la facture (paiement à réception)', permissions=['issue'])
    def issue(self, request, queryset):
        for order in queryset:
            try:
                invoice = issue_invoice(order.pk, request.user, 'Paiement à réception de la facture.')
                self.message_user(request, 'Facture émise : ' + invoice.number)
            except ValidationError as error:
                self.message_user(request, '; '.join(error.messages), messages.ERROR)
    def has_issue_permission(self, request):
        return request.user.has_perm('commerce.add_invoice')

    @admin.action(description='Annuler les commandes sans encaissement', permissions=['cancel'])
    def cancel_selected(self, request, queryset):
        for order in queryset:
            try:
                cancel_order(order.pk, request.user, request.POST.get('reason', ''))
                self.message_user(request, 'Commande annulée : ' + order.number)
            except ValidationError as error:
                self.message_user(request, '; '.join(error.messages), messages.ERROR)
    def has_cancel_permission(self, request):
        return request.user.has_perm('commerce.cancel_order')

class ImmutableAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

@admin.register(Invoice)
class InvoiceAdmin(ImmutableAdmin):
    list_display = ('number', 'order', 'total', 'currency', 'status', 'issued_at')
    list_filter = ('status', 'currency')
    search_fields = ('number', 'customer_name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        with transaction.atomic():
            if request.method == 'POST' and object_id:
                invoice_id = Payment.objects.filter(pk=object_id).values_list('invoice_id', flat=True).first()
                Invoice.objects.select_for_update().filter(pk=invoice_id).first()
                Payment.objects.select_for_update().filter(pk=object_id).first()
            return super().changeform_view(request, object_id, form_url, extra_context)

    list_display = ('reference', 'invoice', 'amount', 'method', 'status', 'confirmed_by')
    list_filter = ('status', 'method')
    readonly_fields = ('status', 'confirmed_at', 'confirmed_by', 'created_at')
    actions = ['confirm']
    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and (obj is None or obj.status == 'pending')
    def has_delete_permission(self, request, obj=None): return False
    @admin.action(description='Confirmer les paiements vérifiés', permissions=['confirm'])
    def confirm(self, request, queryset):
        for payment in queryset:
            try:
                confirm_payment(payment.pk, request.user)
                self.message_user(request, 'Paiement confirmé : ' + payment.reference)
            except ValidationError as error:
                self.message_user(request, '; '.join(error.messages), messages.ERROR)
    def has_confirm_permission(self, request):
        return request.user.has_perm('commerce.confirm_payment')

@admin.register(AuditEvent)
class AuditEventAdmin(ImmutableAdmin):
    list_display = ('created_at', 'actor', 'action', 'target')
    list_filter = ('action',)

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('reference', 'payment', 'amount', 'status', 'confirmed_by')
    readonly_fields = ('status', 'confirmed_at', 'confirmed_by', 'created_at')
    actions = ['confirm']
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and (obj is None or obj.status == 'pending')
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        with transaction.atomic():
            if request.method == 'POST' and object_id:
                info = Refund.objects.filter(pk=object_id).values('payment__invoice__order_id', 'payment__invoice_id', 'payment_id').first()
                if info:
                    Order.objects.select_for_update().filter(pk=info['payment__invoice__order_id']).first()
                    Invoice.objects.select_for_update().filter(pk=info['payment__invoice_id']).first()
                    Payment.objects.select_for_update().filter(pk=info['payment_id']).first()
                    Refund.objects.select_for_update().filter(pk=object_id).first()
            return super().changeform_view(request, object_id, form_url, extra_context)
    @admin.action(description='Confirmer les remboursements effectués', permissions=['confirm'])
    def confirm(self, request, queryset):
        for refund in queryset:
            try:
                confirm_refund(refund.pk, request.user)
                self.message_user(request, 'Remboursement confirmé : ' + refund.reference)
            except ValidationError as error:
                self.message_user(request, '; '.join(error.messages), messages.ERROR)
    def has_confirm_permission(self, request):
        return request.user.has_perm('commerce.confirm_refund')
