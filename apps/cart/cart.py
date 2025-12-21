from decimal import Decimal
from django.conf import settings
from apps.catalog.models import Product

class CartService:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, size=None, quantity=1, update_quantity=False):
        product_id = str(product.id)
        item_key = f"{product_id}_{size}" if size else product_id

        if item_key not in self.cart:
            self.cart[item_key] = {
                'product_id': product.id,
                'name': product.name,
                'quantity': 0,
                'price': str(product.price),
                'size': size,
                'image': product.images.first().image.url if product.images.exists() else '' 
            }
        
        if update_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity
        
        self.save()

    def update_quantity(self, item_key, quantity_change):
        if item_key in self.cart:
            self.cart[item_key]['quantity'] += quantity_change
            if self.cart[item_key]['quantity'] <= 0:
                self.remove(item_key)
            self.save()

    def remove(self, item_key):
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for item_key, item_data in self.cart.items():
            item = item_data.copy()
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['key'] = item_key 
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()
