from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from apps.catalog.models import Product
from .cart import CartService

def cart_detail(request):
    cart = CartService(request)
    return render(request, 'cart/items.html', {
        'cart': cart,
        'total_items': len(cart),
        'total_price': "{:.2f}".format(cart.get_total_price())
    })

@require_POST
def cart_add(request, product_id):
    cart = CartService(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size')
    
    cart.add(product=product, size=size)
    
    response = render(request, 'cart/items.html', {
        'cart': cart,
        'total_items': len(cart),
        'total_price': "{:.2f}".format(cart.get_total_price())
    })
    response['HX-Trigger'] = 'open-add-modal'
    return response

@require_POST
def cart_remove(request, item_key):
    cart = CartService(request)
    cart.remove(item_key)
    
    return render(request, 'cart/items.html', {
        'cart': cart,
        'total_items': len(cart),
        'total_price': "{:.2f}".format(cart.get_total_price())
    })

@require_POST
def cart_update(request, item_key):
    cart = CartService(request)
    action = request.POST.get('action')
    
    if action == 'increment':
        cart.update_quantity(item_key, 1)
    elif action == 'decrement':
        cart.update_quantity(item_key, -1)
        
    return render(request, 'cart/items.html', {
        'cart': cart,
        'total_items': len(cart),
        'total_price': "{:.2f}".format(cart.get_total_price())
    })
