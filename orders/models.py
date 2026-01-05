# orders/models.py

from django.db import models
from django.conf import settings
from vendors.models import Shop
from menu.models import FoodItem

class Cart(models.Model):
    """
    Shopping Cart for Students
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ('user', 'food_item')
    
    def __str__(self):
        return f"{self.user.username} - {self.food_item.name} (x{self.quantity})"
    
    @property
    def total_price(self):
        return self.food_item.price * self.quantity


class Order(models.Model):
    """
    Order Model
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )
    
    # Order Info
    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders')
    
    # Order Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Pricing
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Additional Info
    special_instructions = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"
    
    @property
    def is_active(self):
        return self.status not in ['completed', 'cancelled']


class OrderItem(models.Model):
    """
    Individual items in an order
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        return f"{self.food_item.name} x{self.quantity}"
    
    @property
    def total_price(self):
        return self.price * self.quantity