from django.contrib import admin
from .models import QuoteRequest
from django.core.exceptions import ValidationError
from django.contrib import messages
from apps.commerce.services import convert_quote
@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('reference', 'name', 'service', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'organization')
    readonly_fields = ('reference', 'customer', 'created_at')

    actions = ['convert']
    @admin.action(description='Convertir en commande brouillon', permissions=['convert'])
    def convert(self, request, queryset):
        for quote in queryset:
            try:
                order = convert_quote(quote.pk, request.user)
                self.message_user(request, 'Commande : ' + order.number)
            except ValidationError as error:
                self.message_user(request, '; '.join(error.messages), messages.ERROR)
    def has_convert_permission(self, request):
        return request.user.has_perm('commerce.add_order')
