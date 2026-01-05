# menu/forms.py

from django import forms
from .models import FoodItem

class FoodItemForm(forms.ModelForm):
    """
    Form for vendors to add/edit food items
    """
    
    class Meta:
        model = FoodItem
        fields = ['category', 'name', 'description', 'price', 'image', 
                  'is_available', 'is_vegetarian', 'is_vegan', 'preparation_time']
        
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Chicken Burger'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your food item...'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'preparation_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutes'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_vegetarian': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_vegan': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        
        labels = {
            'name': 'Food Item Name',
            'description': 'Description',
            'price': 'Price (₹)',
            'image': 'Food Image',
            'is_available': 'Available for orders',
            'is_vegetarian': 'Vegetarian',
            'is_vegan': 'Vegan',
            'preparation_time': 'Preparation Time (minutes)',
        }