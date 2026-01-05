# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Home & Authentication
    path('', views.home, name='home'),
    path('register/student/', views.student_register, name='student_register'),
    path('register/vendor/', views.vendor_register, name='vendor_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Profile & Settings
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('settings/', views.settings, name='settings'),
    path('settings/change-password/', views.change_password, name='change_password'),
    path('settings/delete-account/', views.delete_account, name='delete_account'),
]