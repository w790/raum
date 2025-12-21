from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .services import OrderService
from .tasks import send_order_creation_email

@require_http_methods(['GET', 'POST'])
def order_create(request):
    order_service = OrderService(request)
    is_htmx = request.headers.get('HX-Request')
    
    if request.method == 'POST':
        order_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'postal_code': request.POST.get('postal_code'),
            'city': request.POST.get('city'),
        }
        
        if all(order_data.values()):
            order = order_service.create_order(order_data)
            request.session['order_id'] = order.id
            
            send_order_creation_email.delay(order.id)
            
            if is_htmx:
                response = HttpResponse()
                response['HX-Redirect'] = reverse('payments:process')
                return response
            return redirect('payments:process')
    
    context = {
        'cart': order_service.cart,
        'is_htmx': is_htmx
    }
    
    if is_htmx:
        return render(request, 'orders/partials/checkout_content.html', context)
    return render(request, 'orders/checkout.html', context)
