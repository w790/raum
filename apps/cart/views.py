from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from apps.catalog.models import Product
from .services import CartService

def cart_detail(request):
    """
    Returns HTML contents of the cart (for modal).
    """
    cart = CartService(request)
    return render(request, 'catalog/partials/cart_items.html', {
        'cart': cart.cart, # Sending the raw dict for template compatibility
        'total_items': len(cart),
        'total_price': "{:.2f}".format(cart.get_total_price())
    })

@require_POST
def cart_add(request, product_id):
    """
    HTMX: Adds item to cart, returns updated bag count.
    """
    cart = CartService(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size')
    
    cart.add(product=product, size=size)
    
    # Return just the count to update the badge OOB
    return HttpResponse(str(len(cart)))

@require_POST
def cart_remove(request, item_key):
    """
    HTMX: Removes item from cart, returns updated cart detail HTML.
    """
    cart = CartService(request)
    cart.remove(item_key)
    
    # Re-render the cart items list
    return render(request, 'catalog/partials/cart_items.html', {
        'cart': cart.cart,
        'total_items': len(cart),
        'total_price': "{:.2f}".format(cart.get_total_price())
    })

@require_POST
def cart_update(request, item_key):
    """
    HTMX: Updates item quantity.
    """
    # Logic for update if needed (not explicitly requested in recent prompts but in tech.md)
    # Implementing placeholder for now as UI for update isn't built yet
    pass
