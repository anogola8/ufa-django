from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import JsonResponse
from core.models import Ward

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def programs(request):
    return render(request, 'core/programs.html')

def contact(request):
    return render(request, 'core/contact.html')

def get_wards(request):
    # API endpoint to get wards for a specific county
    county_id = request.GET.get('county_id')
    if county_id:
        wards = Ward.objects.filter(county_id=county_id).values('id', 'name')
        return JsonResponse(list(wards), safe=False)
    return JsonResponse([], safe=False)

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
