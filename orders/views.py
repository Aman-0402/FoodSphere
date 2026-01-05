# orders/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
import random
import string
from .models import Cart, Order, OrderItem
from menu.models import FoodItem
from vendors.models import Shop

# ============= CART VIEWS =============

@login_required
def view_cart(request):
    """
    View shopping cart
    """
    if not request.user.is_student:
        messages.error(request, 'Only students can use the cart.')
        return redirect('home')
    
    cart_items = Cart.objects.filter(user=request.user).select_related('food_item', 'food_item__shop')
    
    # Calculate totals
    subtotal = sum(item.total_price for item in cart_items)
    total = subtotal  # Can add tax, delivery fee later
    
    # Group items by shop
    shops_dict = {}
    for item in cart_items:
        shop = item.food_item.shop
        if shop not in shops_dict:
            shops_dict[shop] = []
        shops_dict[shop].append(item)
    
    context = {
        'cart_items': cart_items,
        'shops_dict': shops_dict,
        'subtotal': subtotal,
        'total': total,
        'item_count': cart_items.count(),
    }
    return render(request, 'orders/cart.html', context)


@login_required
def add_to_cart(request, food_id):
    """
    Add item to cart
    """
    if not request.user.is_student:
        messages.error(request, 'Only students can add items to cart.')
        return redirect('home')
    
    food_item = get_object_or_404(FoodItem, id=food_id, is_available=True)
    
    # Check if shop is approved
    if not food_item.shop.is_approved:
        messages.error(request, 'This item is not available.')
        return redirect('browse_menu')
    
    # Get or create cart item
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        food_item=food_item,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Increased {food_item.name} quantity to {cart_item.quantity}')
    else:
        messages.success(request, f'{food_item.name} added to cart!')
    
    return redirect('view_cart')


@login_required
def update_cart(request, cart_id):
    """
    Update cart item quantity
    """
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('view_cart')


@login_required
def remove_from_cart(request, cart_id):
    """
    Remove item from cart
    """
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    item_name = cart_item.food_item.name
    cart_item.delete()
    messages.success(request, f'{item_name} removed from cart!')
    return redirect('view_cart')


@login_required
def clear_cart(request):
    """
    Clear all items from cart
    """
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, 'Cart cleared successfully!')
    return redirect('view_cart')


# ============= ORDER VIEWS =============

def generate_order_number():
    """
    Generate unique order number
    """
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.digits, k=4))
    return f"ORD{timestamp}{random_str}"


@login_required
def checkout(request, shop_id):
    """
    Checkout for a specific shop
    """
    if not request.user.is_student:
        messages.error(request, 'Only students can place orders.')
        return redirect('home')
    
    shop = get_object_or_404(Shop, id=shop_id, status='approved', is_active=True)
    
    # Get cart items for this shop only
    cart_items = Cart.objects.filter(
        user=request.user,
        food_item__shop=shop
    ).select_related('food_item')
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty for this shop.')
        return redirect('view_cart')
    
    # Calculate total
    subtotal = sum(item.total_price for item in cart_items)
    total = subtotal
    
    if request.method == 'POST':
        special_instructions = request.POST.get('special_instructions', '')
        
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    order_number=generate_order_number(),
                    user=request.user,
                    shop=shop,
                    total_amount=total,
                    special_instructions=special_instructions,
                    status='pending',
                    payment_status='pending'
                )
                
                # Create order items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        food_item=cart_item.food_item,
                        quantity=cart_item.quantity,
                        price=cart_item.food_item.price
                    )
                
                # Clear cart items for this shop
                cart_items.delete()
                
                messages.success(request, f'Order placed successfully! Order #{order.order_number}')
                return redirect('order_detail', order_id=order.id)
        
        except Exception as e:
            messages.error(request, 'Error placing order. Please try again.')
            return redirect('view_cart')
    
    context = {
        'shop': shop,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def my_orders(request):
    """
    View user's order history
    """
    if request.user.is_student:
        orders = Order.objects.filter(user=request.user).select_related('shop').prefetch_related('items')
    elif request.user.is_vendor:
        try:
            shop = request.user.shop
            orders = Order.objects.filter(shop=shop).select_related('user').prefetch_related('items')
        except:
            messages.error(request, 'You don\'t have a shop.')
            return redirect('dashboard')
    else:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/my_orders.html', context)


@login_required
def order_detail(request, order_id):
    """
    View order details
    """
    if request.user.is_student:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    elif request.user.is_vendor:
        try:
            shop = request.user.shop
            order = get_object_or_404(Order, id=order_id, shop=shop)
        except:
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
    else:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def update_order_status(request, order_id):
    """
    Vendor updates order status
    """
    if not request.user.is_vendor:
        messages.error(request, 'Only vendors can update order status.')
        return redirect('home')
    
    try:
        shop = request.user.shop
        order = get_object_or_404(Order, id=order_id, shop=shop)
    except:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('order_detail', order_id=order.id)


@login_required
def cancel_order(request, order_id):
    """
    Cancel an order
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status in ['completed', 'cancelled']:
        messages.error(request, 'This order cannot be cancelled.')
        return redirect('order_detail', order_id=order.id)
    
    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully.')
        return redirect('my_orders')
    
    return render(request, 'orders/cancel_order.html', {'order': order})