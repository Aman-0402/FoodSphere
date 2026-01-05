# orders/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, Order, OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin interface for Cart
    """
    list_display = ['user', 'food_item', 'quantity', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'food_item__name']
    readonly_fields = ['created_at', 'updated_at']


class OrderItemInline(admin.TabularInline):
    """
    Inline for Order Items
    """
    model = OrderItem
    extra = 0
    readonly_fields = ['food_item', 'quantity', 'price', 'total_price']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Orders
    """
    list_display = ['order_number', 'user', 'shop', 'status_badge', 'payment_badge', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at', 'shop']
    search_fields = ['order_number', 'user__username', 'shop__shop_name']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'shop', 'total_amount')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Additional Info', {
            'fields': ('special_instructions',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'preparing': 'purple',
            'ready': 'green',
            'completed': 'darkgreen',
            'cancelled': 'red',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def payment_badge(self, obj):
        colors = {
            'pending': 'orange',
            'paid': 'green',
            'failed': 'red',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px;">{}</span>',
            colors.get(obj.payment_status, 'gray'),
            obj.get_payment_status_display()
        )
    payment_badge.short_description = 'Payment'