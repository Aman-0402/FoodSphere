# menu/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import FoodItem, Category
from .forms import FoodItemForm
from vendors.models import Shop

# ============= VENDOR VIEWS =============

@login_required
def vendor_menu_list(request):
    """
    List all food items for the logged-in vendor
    """
    if not request.user.is_vendor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        shop = request.user.shop
        if not shop.is_approved:
            messages.warning(request, 'Your shop is not approved yet.')
            return redirect('vendor_shop_detail')
    except Shop.DoesNotExist:
        messages.error(request, 'You don\'t have a shop yet.')
        return redirect('apply_shop')
    
    food_items = FoodItem.objects.filter(shop=shop).select_related('category')
    
    context = {
        'shop': shop,
        'food_items': food_items,
    }
    return render(request, 'menu/vendor_menu_list.html', context)


@login_required
def vendor_add_food(request):
    """
    Vendor adds a new food item
    """
    if not request.user.is_vendor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        shop = request.user.shop
        if not shop.is_approved:
            messages.warning(request, 'Your shop must be approved first.')
            return redirect('vendor_shop_detail')
    except Shop.DoesNotExist:
        messages.error(request, 'You don\'t have a shop yet.')
        return redirect('apply_shop')
    
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.shop = shop
            food_item.save()
            messages.success(request, f'{food_item.name} added successfully!')
            return redirect('vendor_menu_list')
    else:
        form = FoodItemForm()
    
    return render(request, 'menu/vendor_add_food.html', {'form': form})


@login_required
def vendor_edit_food(request, food_id):
    """
    Vendor edits a food item
    """
    if not request.user.is_vendor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        messages.error(request, 'You don\'t have a shop yet.')
        return redirect('apply_shop')
    
    food_item = get_object_or_404(FoodItem, id=food_id, shop=shop)
    
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            form.save()
            messages.success(request, f'{food_item.name} updated successfully!')
            return redirect('vendor_menu_list')
    else:
        form = FoodItemForm(instance=food_item)
    
    return render(request, 'menu/vendor_edit_food.html', {'form': form, 'food_item': food_item})


@login_required
def vendor_delete_food(request, food_id):
    """
    Vendor deletes a food item
    """
    if not request.user.is_vendor:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        shop = request.user.shop
    except Shop.DoesNotExist:
        messages.error(request, 'You don\'t have a shop yet.')
        return redirect('apply_shop')
    
    food_item = get_object_or_404(FoodItem, id=food_id, shop=shop)
    
    if request.method == 'POST':
        food_name = food_item.name
        food_item.delete()
        messages.success(request, f'{food_name} deleted successfully!')
        return redirect('vendor_menu_list')
    
    return render(request, 'menu/vendor_delete_food.html', {'food_item': food_item})


# ============= PUBLIC/STUDENT VIEWS =============

def browse_menu(request):
    """
    Browse all available food items
    """
    food_items = FoodItem.objects.filter(
        shop__status='approved',
        shop__is_active=True,
        is_available=True
    ).select_related('shop', 'category')
    
    categories = Category.objects.filter(is_active=True)
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        food_items = food_items.filter(category__id=category_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        food_items = food_items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(shop__shop_name__icontains=search_query)
        )
    
    # Filter by dietary preferences
    if request.GET.get('vegetarian'):
        food_items = food_items.filter(is_vegetarian=True)
    if request.GET.get('vegan'):
        food_items = food_items.filter(is_vegan=True)
    
    context = {
        'food_items': food_items,
        'categories': categories,
        'selected_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'menu/browse_menu.html', context)


def food_detail(request, food_id):
    """
    Detailed view of a food item
    """
    food_item = get_object_or_404(
        FoodItem,
        id=food_id,
        shop__status='approved',
        shop__is_active=True
    )
    
    # Get related items from same shop
    related_items = FoodItem.objects.filter(
        shop=food_item.shop,
        is_available=True
    ).exclude(id=food_item.id)[:4]
    
    context = {
        'food_item': food_item,
        'related_items': related_items,
    }
    return render(request, 'menu/food_detail.html', context)


def shop_menu(request, shop_id):
    """
    View all food items from a specific shop
    """
    shop = get_object_or_404(Shop, id=shop_id, status='approved', is_active=True)
    food_items = FoodItem.objects.filter(shop=shop, is_available=True).select_related('category')
    categories = Category.objects.filter(is_active=True, food_items__shop=shop).distinct()
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        food_items = food_items.filter(category__id=category_filter)
    
    context = {
        'shop': shop,
        'food_items': food_items,
        'categories': categories,
        'selected_category': category_filter,
    }
    return render(request, 'menu/shop_menu.html', context)