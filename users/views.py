from django.contrib import auth, messages
from django.shortcuts import render, redirect
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from events.models import EventRegistration


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                auth.login(request, user)
                messages.success(request, 'Добро пожаловать!')
                return redirect('index')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация успешна! Войдите в аккаунт.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def logout(request):
    auth.logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('index')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)

    # Последние 5 бронирований
    registrations = EventRegistration.objects.filter(
        user=request.user
    ).select_related('event').order_by('-registration_timestamp')[:5]

    return render(request, 'users/profile.html', {
        'form': form,
        'registrations': registrations
    })