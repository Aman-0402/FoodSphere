# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, VendorRegistrationForm, UserLoginForm
from .models import User

def home(request):
    """
    Home page view
    """
    return render(request, 'home.html')


def student_register(request):
    """
    Student registration view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/student_register.html', {'form': form})


def vendor_register(request):
    """
    Vendor registration view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Vendor account created! Admin will review your application.')
            return redirect('login')
    else:
        form = VendorRegistrationForm()
    
    return render(request, 'accounts/vendor_register.html', {'form': form})


def user_login(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """
    User logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


# ==================== PROFILE & SETTINGS VIEWS ====================

@login_required
def profile(request):
    """
    User profile view
    """
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    """
    Edit user profile
    """
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        
        # Handle profile picture upload
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'accounts/edit_profile.html')


@login_required
def settings(request):
    """
    User settings view
    """
    return render(request, 'accounts/settings.html')


@login_required
def change_password(request):
    """
    Change user password
    """
    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Verify old password
        if not user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')
        
        # Check if new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')
        
        # Check password length
        if len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('change_password')
        
        # Set new password
        user.set_password(new_password1)
        user.save()
        
        messages.success(request, 'Password changed successfully! Please login again.')
        return redirect('login')
    
    return render(request, 'accounts/change_password.html')


@login_required
def delete_account(request):
    """
    Delete user account
    """
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Verify password
        if not request.user.check_password(password):
            messages.error(request, 'Incorrect password.')
            return redirect('delete_account')
        
        # Delete account
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')
    
    return render(request, 'accounts/delete_account.html')