from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from apps.orders.models import Order
from apps.orders.tasks import send_payment_confirmation_email
from .services import NowPaymentsService
from .models import PaymentTransaction
import json

def payment_process(request):
    order_id = request.session.get('order_id')
    user_q = Q(user=request.user) if request.user.is_authenticated else Q(user__isnull=True)
    session_q = Q(session_key=request.session.session_key)
    
    order = get_object_or_404(Order, Q(id=order_id) & (user_q | session_q))
    payment_service = NowPaymentsService()
    
    scheme = "https" if request.is_secure() else "http"
    domain = request.get_host()
    
    success_url = f"{scheme}://{domain}/payments/done/"
    cancel_url = f"{scheme}://{domain}/payments/canceled/"
    ipn_url = f"{scheme}://{domain}/payments/webhook/"
    
    invoice = payment_service.create_invoice(order, success_url, cancel_url, ipn_url)
    order.payment_id = invoice.get('id')
    order.save()
    
    PaymentTransaction.objects.create(
        order=order,
        payment_id=invoice.get('id'),
        status='created',
        amount=order.total_price,
        currency='USD',
        payload=invoice
    )
    
    return redirect(invoice.get('invoice_url'))

def payment_done(request):
    is_htmx = request.headers.get('HX-Request')
    context = {'is_htmx': is_htmx}
    if is_htmx:
        return render(request, 'payments/partials/done_content.html', context)
    return render(request, 'payments/done.html', context)

def payment_canceled(request):
    is_htmx = request.headers.get('HX-Request')
    context = {'is_htmx': is_htmx}
    if is_htmx:
        return render(request, 'payments/partials/canceled_content.html', context)
    return render(request, 'payments/canceled.html', context)

def payment_pending(request):
    is_htmx = request.headers.get('HX-Request')
    context = {'is_htmx': is_htmx}
    if is_htmx:
        return render(request, 'payments/partials/pending_content.html', context)
    return render(request, 'payments/pending.html', context)

@csrf_exempt
@require_POST
def payment_webhook(request):
    signature = request.headers.get('x-nowpayments-sig')
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)
    
    payment_service = NowPaymentsService()
    if payment_service.verify_ipn_signature(signature, payload):
        order_id = payload.get('order_id')
        payment_status = payload.get('payment_status')
        payment_id = payload.get('payment_id')
        
        order = get_object_or_404(Order, id=order_id)
        
        PaymentTransaction.objects.update_or_create(
            payment_id=payment_id,
            defaults={
                'order': order,
                'status': payment_status,
                'amount': payload.get('actually_paid', order.total_price),
                'currency': payload.get('pay_currency', 'USD'),
                'payload': payload
            }
        )
        
        if payment_status == 'finished':
            order.status = 'paid'
            order.save()
            send_payment_confirmation_email.delay(order.id)
            return HttpResponse(status=200)
        
        return HttpResponse(status=200)
    
    return HttpResponse(status=400)
