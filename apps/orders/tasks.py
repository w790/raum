from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@shared_task
def send_order_creation_email(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order #{order.id} Created'
    message = (
        f'Hello {order.first_name},\n\n'
        f'An order has been created with your email.\n'
        f'To complete your purchase, please finish the payment.\n\n'
        f'Order Total: ${order.total_price}\n'
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )

@shared_task
def send_payment_confirmation_email(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Payment Confirmed for Order #{order.id}'
    message = (
        f'Hello {order.first_name},\n\n'
        f'We have successfully received your payment for order #{order.id}.\n'
        f'Your order is now being processed.\n\n'
        f'Thank you for shopping with RAÚM.'
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )
