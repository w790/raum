from decimal import Decimal
from django.conf import settings
from apps.catalog.models import Product

class CartService:
    def __init__(self, request):
        """
        Initialize the cart using the session.
        """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, size=None, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        # Unique key composition
        item_key = f"{product_id}_{size}" if size else product_id

        if item_key not in self.cart:
            self.cart[item_key] = {
                'product_id': product.id,
                'name': product.name,
                'quantity': 0,
                'price': str(product.price),
                'size': size,
                # Store enough info to render without DB hit if possible, 
                # though views might fetch fresh main image
                'image': product.images.first().image.url if product.images.exists() else '' 
            }
        
        if update_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity
        
        self.save()

    def remove(self, item_key):
        """
        Remove a product from the cart.
        """
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def save(self):
        # Mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        # Note: For simple rendering we might rely on stored session data, 
        # but for robustness it's often good to re-fetch or just yield the dicts.
        # Given Requirements 'N+1 problem', if we needed objects we would fetch them.
        # For now, yielding the dicts from session is sufficient and fast for the modal.
        for item_key, item in self.cart.items():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['key'] = item_key 
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()
