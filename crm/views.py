from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required


def homepage(request):
    return render(request, 'crm/index.html')


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect("login")
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)  # Debugging output

    else:
        form = CreateUserForm()

    context = {'registerform': form}

    return render(request, 'crm/register.html', context=context)


def my_login(request):

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, 'Invalid username or password.')

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = LoginForm()

    context = {'loginform': form}

    return render(request, 'crm/my-login.html', context=context)


def user_logout(request):

    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')

    return redirect("")


@login_required(login_url="login")
def dashboard(request):
    return render(request, 'crm/dashboard.html')