from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog_list, name='list'),
    path('category/<slug:slug>/', views.catalog_list, name='list_category'),
    path('product/<slug:slug>/', views.product_detail, name='detail'),
    path('search/', views.search_products, name='search'),
]
