from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import SignupForm, CustomLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random

def send_whatsapp_code(phone, code):
    print(f"Sending WhatsApp code {code} to {phone}")
    # Placeholder – integrate Termii or Twilio API here

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            code = str(random.randint(100000, 999999))
            user.verification_code = code
            user.is_active = False
            user.save()
            send_whatsapp_code(user.phone_number, code)
            return redirect('verify', user_id=user.id)
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def verify_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == user.verification_code:
            user.is_verified = True
            user.is_active = True
            user.save()
            return redirect('login')
    return render(request, 'users/verify.html', {'user': user})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_verified:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'users/login.html', {'form': form, 'error': 'Please verify your account first.'})
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
