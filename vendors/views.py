# vendors/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Shop
from .forms import ShopApplicationForm, ShopUpdateForm
from menu.models import FoodItem  # Add this import

@login_required
def apply_shop(request):
    """
    View for vendors to apply for a shop
    """
    # Check if user is a vendor
    if not request.user.is_vendor:
        messages.error(request, 'Only vendors can apply for shops.')
        return redirect('home')
    
    # Check if vendor already has a shop
    if hasattr(request.user, 'shop'):
        messages.info(request, 'You already have a shop application.')
        return redirect('vendor_shop_detail')
    
    if request.method == 'POST':
        form = ShopApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.vendor = request.user
            shop.save()
            messages.success(request, 'Shop application submitted successfully! Admin will review it soon.')
            return redirect('vendor_shop_detail')
    else:
        form = ShopApplicationForm()
    
    return render(request, 'vendors/apply_shop.html', {'form': form})


@login_required
def vendor_shop_detail(request):
    """
    View vendor's shop details and status
    """
    if not request.user.is_vendor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        messages.info(request, 'You haven\'t applied for a shop yet.')
        return redirect('apply_shop')
    
    return render(request, 'vendors/shop_detail.html', {'shop': shop})


@login_required
def vendor_shop_update(request):
    """
    Update shop details
    """
    if not request.user.is_vendor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        messages.error(request, 'You don\'t have a shop yet.')
        return redirect('apply_shop')
    
    if request.method == 'POST':
        form = ShopUpdateForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shop details updated successfully!')
            return redirect('vendor_shop_detail')
    else:
        form = ShopUpdateForm(instance=shop)
    
    return render(request, 'vendors/shop_update.html', {'form': form, 'shop': shop})


def shop_list(request):
    """
    Public view to list all approved shops
    """
    shops = Shop.objects.filter(status='approved', is_active=True)
    return render(request, 'vendors/shop_list.html', {'shops': shops})


def shop_public_detail(request, shop_id):
    """
    Public view of a shop's details with menu items
    """
    shop = get_object_or_404(Shop, id=shop_id, status='approved', is_active=True)
    
    # Get food items from this shop (limit to 6 for preview)
    food_items = FoodItem.objects.filter(
        shop=shop, 
        is_available=True
    ).select_related('category')[:6]
    
    # Get total count
    total_items = FoodItem.objects.filter(shop=shop, is_available=True).count()
    
    context = {
        'shop': shop,
        'food_items': food_items,
        'total_items': total_items,
    }
    return render(request, 'vendors/shop_public_detail.html', context)