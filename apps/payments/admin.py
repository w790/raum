from django.contrib import admin
from .models import PaymentTransaction

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'order', 'status', 'amount', 'currency', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['payment_id', 'order__id', 'order__email']
    readonly_fields = ['created_at', 'updated_at', 'payload']
