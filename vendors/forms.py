# vendors/forms.py

from django import forms
from .models import Shop

class ShopApplicationForm(forms.ModelForm):
    """
    Form for vendors to apply for a shop
    """
    
    class Meta:
        model = Shop
        fields = ['shop_name', 'description', 'shop_logo', 'shop_banner', 'phone', 'email', 'address']
        widgets = {
            'shop_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your shop name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your food business...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 1234567890'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'shop@example.com'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Shop address or location...'
            }),
            'shop_logo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'shop_banner': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'shop_name': 'Shop Name',
            'description': 'Shop Description',
            'shop_logo': 'Shop Logo (Optional)',
            'shop_banner': 'Shop Banner (Optional)',
            'phone': 'Contact Phone',
            'email': 'Contact Email',
            'address': 'Shop Address/Location',
        }


class ShopUpdateForm(forms.ModelForm):
    """
    Form for vendors to update their shop details
    """
    
    class Meta:
        model = Shop
        fields = ['shop_name', 'description', 'shop_logo', 'shop_banner', 'phone', 'email', 'address']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'shop_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'shop_banner': forms.FileInput(attrs={'class': 'form-control'}),
        }