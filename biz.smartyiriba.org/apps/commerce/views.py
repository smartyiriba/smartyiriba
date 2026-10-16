from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Order, Invoice, Refund

@login_required
def orders(request):
    return render(request, 'commerce/orders.html', {'orders': Order.objects.filter(customer=request.user).exclude(status='draft').prefetch_related('lines')})

@login_required
def invoice_detail(request, number):
    invoice = get_object_or_404(Invoice.objects.select_related('order'), number=number, order__customer=request.user)
    return render(request, 'commerce/invoice.html', {'invoice': invoice, 'payments': invoice.payments.all(), 'refunds': Refund.objects.filter(payment__invoice=invoice, status=Refund.Status.CONFIRMED)})

@login_required
def invoice_download(request, number):
    from django.http import HttpResponse
    from .pdf import invoice_pdf
    invoice = get_object_or_404(Invoice.objects.select_related('order'), number=number, order__customer=request.user)
    response = HttpResponse(invoice_pdf(invoice), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + invoice.number + '.pdf"'
    response['Cache-Control'] = 'private, no-store'
    return response
