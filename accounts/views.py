from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm
from .models import Profile


def client_ip(request):
    try:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except Exception:
        ip = ""
    return ip


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                profile = Profile.objects.get(user=user)
                profile.ip = client_ip(request)
                profile.save()
            except Profile.DoesNotExist:
                pass
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')
