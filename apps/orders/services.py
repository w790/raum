from django.db import transaction
from .models import Order, OrderItem
from apps.cart.cart import CartService

class OrderService:
    def __init__(self, request):
        self.request = request
        self.cart = CartService(request)

    @transaction.atomic
    def create_order(self, order_data):
        order = Order.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            first_name=order_data.get('first_name'),
            last_name=order_data.get('last_name'),
            email=order_data.get('email'),
            address=order_data.get('address'),
            postal_code=order_data.get('postal_code'),
            city=order_data.get('city'),
            session_key=self.request.session.session_key,
            total_price=self.cart.get_total_price()
        )
        
        for item in self.cart:
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price_at_purchase=item['price']
            )
        
        self.cart.clear()
        return order
