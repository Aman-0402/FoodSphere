# vendors/models.py

from django.db import models
from django.conf import settings

class Shop(models.Model):
    """
    Vendor Shop Model
    Each vendor can have one shop
    """
    
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    )
    
    vendor = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='shop',
        limit_choices_to={'role': 'vendor'}
    )
    
    # Shop Details
    shop_name = models.CharField(max_length=200)
    description = models.TextField()
    shop_logo = models.ImageField(upload_to='shops/logos/', blank=True, null=True)
    shop_banner = models.ImageField(upload_to='shops/banners/', blank=True, null=True)
    
    # Contact Information
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    
    # Shop Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=False)
    
    # Admin Notes
    admin_notes = models.TextField(blank=True, null=True, help_text="Admin's notes about this shop")
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.shop_name} - {self.vendor.username}"
    
    @property
    def is_approved(self):
        return self.status == 'approved' and self.is_active
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_rejected(self):
        return self.status == 'rejected'
    
    @property
    def is_blocked(self):
        return self.status == 'blocked'