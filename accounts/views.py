from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import RegisterForm, ProfileForm, ProfileUpdateForm
from members.models import Member


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Welcome to UFA! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            # Admin users go to executive dashboard
            return reverse('dashboard:executive')
        else:
            # Regular users go to member dashboard
            return reverse('dashboard:member')


def logout_view(request):
    """Log out user and redirect to home page"""
    auth_logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')


@login_required
def profile(request):
    """View and update user profile"""
    # Get or create member profile
    try:
        member = request.user.member_profile
    except Member.DoesNotExist:
        # Create a member profile if it doesn't exist
        member = Member.objects.create(
            user=request.user,
            full_name=f"{request.user.first_name} {request.user.last_name}",
            email=request.user.email,
            membership_status='pending',
            membership_type='youth'
        )
        messages.info(request, 'Your member profile has been created. Please complete your details.')
    
    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=member)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = ProfileForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=member)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'member': member
    })


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            if user.is_staff or user.is_superuser:
                return redirect('dashboard:executive')
            else:
                return redirect('dashboard:member')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/custom_login.html')
