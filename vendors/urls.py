# vendors/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Vendor Shop Management
    path('apply/', views.apply_shop, name='apply_shop'),
    path('my-shop/', views.vendor_shop_detail, name='vendor_shop_detail'),
    path('my-shop/update/', views.vendor_shop_update, name='vendor_shop_update'),
    
    # Public Shop Views
    path('shops/', views.shop_list, name='shop_list'),
    path('shop/<int:shop_id>/', views.shop_public_detail, name='shop_public_detail'),
]