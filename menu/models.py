# menu/models.py

from django.db import models
from vendors.models import Shop

class Category(models.Model):
    """
    Food Categories (Snacks, Meals, Drinks, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class FoodItem(models.Model):
    """
    Food Items that vendors can add to their menu
    """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='food_items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='food_items')
    
    # Food Details
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_items/', blank=True, null=True)
    
    # Availability
    is_available = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    
    # Additional Info
    preparation_time = models.IntegerField(help_text="Time in minutes", blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Food Item'
        verbose_name_plural = 'Food Items'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.shop.shop_name}"
    
    @property
    def is_in_stock(self):
        return self.is_available and self.shop.is_approved