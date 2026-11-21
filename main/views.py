from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import ProfileForm


def home(request):
    return render(request, 'main/home.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد. خوش آمدید!')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'با موفقیت وارد حساب کاربری شدید.')
            return redirect('home')
        messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = AuthenticationForm()

    return render(request, 'main/login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت از حساب کاربری خارج شدید.')
    return redirect('home')


@login_required(login_url='login')
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات پروفایل با موفقیت ذخیره شد.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'main/profile.html', {'form': form})
