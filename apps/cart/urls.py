from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('detail/', views.cart_detail, name='detail'),
    path('add/<int:product_id>/', views.cart_add, name='add'),
    path('update/<str:item_key>/', views.cart_update, name='update'),
    path('remove/<str:item_key>/', views.cart_remove, name='remove'),
]
