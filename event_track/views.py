from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from .forms import UserRegistrationForm, UserUpdateForm

# from rest_framework.decorators import api_view


# Create your views here.
def event_home(request):
    current_user = str(request.user)
    print(current_user)
    request.session['previous_page'] = 'event_home'
    if current_user == 'AnonymousUser':
        return render(request, 'event_track_home.html', {'user': None})
    
    return render(request, 'event_track_home.html', {'user': current_user})

def authorize_user(request):
    current_user = str(request.user)
    previous_page = request.session['previous_page']

    if current_user == 'AnonymousUser':
        login_form = AuthenticationForm()
        if request.method == 'POST':
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('event_home')
            
        return render(request, 'user_login.html', {'login_form': login_form})

    else:
        return redirect('event_home')

def unauthorize_user(request):
    user = str(request.user)
    print(user)
    if user == 'AnonymousUser':
        return render(request, 'user_logout.html', {'user': None})

    logout(request)
    return render(request, 'user_logout.html', {'user': user})

def register_user(request):
    registration_form = UserRegistrationForm()

    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('authorize_user')

    return render(request, 'user_registration.html', {'registration_form': registration_form})

def user_profile(request):
    user = str(request.user)
    if user != 'AnonymousUser':
        return render(request, 'user_profile.html', {'user': request.user})

def update_user(request):
    username = str(request.user)
    if username != 'AnonymousUser':
        user = User.objects.get(username=username)
        if request.method == 'POST':
            form = UserUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()

        else:
            form = UserUpdateForm(instance=user)
            return render(request, 'user_update.html', {'user_profile_form': form})
    
    return redirect('authorize_user')