from django.contrib import messages

from django.shortcuts import render, redirect

from .forms import CreateUserForm


def homepage(request):
    return render(request, 'crm/index.html')


def register(request):

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect("my-login")
        else:
            messages.error(request, 'Please correct the errors below.')
            print(form.errors)  # Debugging output
    else:
        form = CreateUserForm()

    context = {'registerform':form}

    return render(request, 'crm/register.html', context=context)


def my_login(request):
    return render(request, 'crm/my-login.html')


def dashboard(request):
    return render(request, 'crm/dashboard.html')
