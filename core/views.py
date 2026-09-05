from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def programs(request):
    return render(request, 'core/programs.html')

def contact(request):
    return render(request, 'core/contact.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard:executive')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/custom_login.html')

def test_login(request):
    return render(request, 'core/test-login.html')

def test_icons(request):
    return render(request, 'core/test.html')
