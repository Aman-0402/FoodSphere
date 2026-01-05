# vendors/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Shop

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """
    Admin interface for Shop management
    """
    list_display = ['shop_name', 'vendor_username', 'status_badge', 'phone', 'applied_at', 'action_buttons']
    list_filter = ['status', 'is_active', 'applied_at']
    search_fields = ['shop_name', 'vendor__username', 'vendor__email', 'phone']
    readonly_fields = ['applied_at', 'approved_at', 'updated_at', 'vendor']
    
    fieldsets = (
        ('Shop Information', {
            'fields': ('vendor', 'shop_name', 'description', 'shop_logo', 'shop_banner')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Status & Approval', {
            'fields': ('status', 'is_active', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'approved_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def vendor_username(self, obj):
        return obj.vendor.username
    vendor_username.short_description = 'Vendor'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red',
            'blocked': 'gray',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def action_buttons(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="/admin/vendors/shop/{}/change/" style="background-color: green; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">Review</a>',
                obj.id
            )
        return '-'
    action_buttons.short_description = 'Actions'
    
    def save_model(self, request, obj, form, change):
        # Auto-set approved_at when status changes to approved
        if obj.status == 'approved' and not obj.approved_at:
            obj.approved_at = timezone.now()
            obj.is_active = True
        
        # Deactivate if rejected or blocked
        if obj.status in ['rejected', 'blocked']:
            obj.is_active = False
        
        super().save_model(request, obj, form, change)