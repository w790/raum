from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .services import OrderService

@require_POST
def order_create(request):
    order_service = OrderService(request)
    if not order_service.cart:
        return redirect('catalog:list')
    
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
        return redirect('payments:process')
    
    return redirect('catalog:list')
