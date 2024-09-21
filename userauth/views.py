from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = UserRegistrationForm()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Account created for {form.cleaned_data["username"]}')
                return redirect('login')
        return render (request, "register.html",{'form' : form})

def loginform(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = UserLoginForm()

        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, "Username or password is incorrect.")

        return render (request, "login.html",{'form' : form})

def logoutform(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    return render(request, "dashboard.html", {user : user})