# orders/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Cart URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    # Order URLs
    path('checkout/<int:shop_id>/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
]