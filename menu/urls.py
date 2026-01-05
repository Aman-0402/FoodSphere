# menu/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Vendor Menu Management
    path('vendor/menu/', views.vendor_menu_list, name='vendor_menu_list'),
    path('vendor/menu/add/', views.vendor_add_food, name='vendor_add_food'),
    path('vendor/menu/edit/<int:food_id>/', views.vendor_edit_food, name='vendor_edit_food'),
    path('vendor/menu/delete/<int:food_id>/', views.vendor_delete_food, name='vendor_delete_food'),
    
    # Public/Student Views
    path('browse/', views.browse_menu, name='browse_menu'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),
    path('shop/<int:shop_id>/menu/', views.shop_menu, name='shop_menu'),
]