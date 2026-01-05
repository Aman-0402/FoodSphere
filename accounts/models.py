# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User Model with role-based access
    Roles: Admin, Vendor, Student
    """
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('student', 'Student'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    @property
    def is_vendor(self):
        return self.role == 'vendor'
    
    @property
    def is_student(self):
        return self.role == 'student'