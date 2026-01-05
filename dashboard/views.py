# dashboard/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from vendors.models import Shop
from menu.models import FoodItem
from orders.models import Order

@login_required
def dashboard(request):
    """
    Role-based dashboard view
    """
    user = request.user
    
    # Admin Dashboard
    if user.is_admin:
        context = {
            'total_vendors': Shop.objects.count(),
            'pending_shops': Shop.objects.filter(status='pending').count(),
            'approved_shops': Shop.objects.filter(status='approved').count(),
            'total_food_items': FoodItem.objects.count(),
            'total_orders': Order.objects.count(),
        }
        return render(request, 'dashboard/admin_dashboard.html', context)
    
    # Vendor Dashboard
    elif user.is_vendor:
        try:
            shop = user.shop
            today_orders = Order.objects.filter(
                shop=shop, 
                created_at__date=timezone.now().date()
            )
            context = {
                'shop': shop,
                'total_food_items': FoodItem.objects.filter(shop=shop).count(),
                'available_items': FoodItem.objects.filter(shop=shop, is_available=True).count(),
                'total_orders': Order.objects.filter(shop=shop).count(),
                'today_orders': today_orders.count(),
                'pending_orders': Order.objects.filter(shop=shop, status='pending').count(),
            }
            return render(request, 'dashboard/vendor_dashboard.html', context)
        except Shop.DoesNotExist:
            messages.info(request, 'Please apply for a shop first.')
            return redirect('apply_shop')
    
    # Student Dashboard
    elif user.is_student:
        context = {
            'total_shops': Shop.objects.filter(status='approved', is_active=True).count(),
            'total_food_items': FoodItem.objects.filter(is_available=True, shop__status='approved').count(),
            'my_orders': Order.objects.filter(user=user).count(),
            'active_orders': Order.objects.filter(
                user=user, 
                status__in=['pending', 'confirmed', 'preparing', 'ready']
            ).count(),
        }
        return render(request, 'dashboard/student_dashboard.html', context)
    
    # Default (shouldn't reach here normally)
    return render(request, 'dashboard/dashboard.html')