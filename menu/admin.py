# menu/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, FoodItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Categories
    """
    list_display = ['name', 'icon', 'is_active', 'food_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    
    def food_count(self, obj):
        return obj.food_items.count()
    food_count.short_description = 'Total Items'


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    """
    Admin interface for Food Items
    """
    list_display = ['name', 'shop', 'category', 'price', 'is_available', 'availability_badge', 'dietary_info', 'created_at']
    list_filter = ['is_available', 'is_vegetarian', 'is_vegan', 'category', 'created_at']
    search_fields = ['name', 'shop__shop_name', 'description']
    list_editable = ['is_available']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('shop', 'category', 'name', 'description', 'image')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'is_available', 'preparation_time')
        }),
        ('Dietary Information', {
            'fields': ('is_vegetarian', 'is_vegan')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def availability_badge(self, obj):
        if obj.is_available:
            return format_html(
                '<span style="background-color: green; color: white; padding: 3px 10px; border-radius: 5px;">Available</span>'
            )
        return format_html(
            '<span style="background-color: red; color: white; padding: 3px 10px; border-radius: 5px;">Unavailable</span>'
        )
    availability_badge.short_description = 'Status'
    
    def dietary_info(self, obj):
        badges = []
        if obj.is_vegetarian:
            badges.append('<span style="background-color: green; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">🌱 VEG</span>')
        if obj.is_vegan:
            badges.append('<span style="background-color: darkgreen; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">🥬 VEGAN</span>')
        return format_html(' '.join(badges)) if badges else '-'
    dietary_info.short_description = 'Dietary'