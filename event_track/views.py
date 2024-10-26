from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UserUpdateForm, EventForm
from .models import Event, BookedEvent

# from rest_framework.decorators import api_view


# Create your views here.
def event_home(request):
    current_user = request.user
    events = Event.objects.all()
    request.session['previous_page'] = 'event_home'
    if str(current_user) == 'AnonymousUser':
        return render(request, 'event_track_home.html', {'user': None, 'events': events})
    
    booked_event_ids = set(Event.objects.filter(booked_events__user=current_user).values_list('id', flat=True))
    return render(request, 'event_track_home.html', {'user': current_user, 'events': events, 'booked_event_ids': booked_event_ids})


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


@login_required
def user_profile(request):
    user = str(request.user)
    if user != 'AnonymousUser':
        return render(request, 'user_profile.html', {'user': request.user})


@login_required
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


@login_required
def add_event(request):
    current_user = request.user
    event_form = EventForm()
    
    if request.method == 'POST':
        event_form = EventForm(data=request.POST)
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.organizer = current_user
            event.save()
            return redirect('event_home')

    return render(request, 'event_add.html', {'event_form': event_form, 'user': current_user})


def event_details(request, id):
    try:
        event = Event.objects.get(pk=id)
        return render(request, 'event_details.html', {'event': event})
    except Event.DoesNotExist:
        return render(request, 'event_not_found.html')
    

@login_required
def my_events(request):
    current_user = request.user
    events = Event.objects.filter(organizer=current_user).all()
    if str(current_user) == 'admin':
        events = Event.objects.all()

    return render(request, 'event_mine.html', {'events': events})


@login_required
def update_event(request, id):
    current_user = request.user
    try:
        event = Event.objects.get(pk=id)
        if str(current_user) != 'admin':
            events = Event.objects.filter(organizer=current_user).values_list('id', flat=True)
            event_ids = set(events)
            if id not in event_ids:
                return render(request, 'event_permission.html')
        
        form = EventForm(instance=event)
        if request.method == 'POST':
            form = EventForm(data=request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('my_events')
        
        return render(request, 'event_update.html', {'event_form': form})
    
    except Event.DoesNotExist:
        return render(request, 'event_not_found.html')
    

@login_required
def delete_event(request, id):
    current_user = request.user
    try:
        event = Event.objects.get(pk=id)
        if str(current_user) != 'admin':
            events = Event.objects.filter(organizer=current_user).values_list('id', flat=True)
            event_ids = set(events)
            if id not in event_ids:
                return render(request, 'event_permission.html')
            else:
                event.delete()
                return redirect('event_home')
        else:
            event.delete()
            return redirect('event_home')
    except Event.DoesNotExist:
        return render(request, 'event_not_found.html')
    

@login_required
def book_an_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        if event.is_full:
            return render(request, 'event_fully_booked.html')
        
        booking = BookedEvent.objects.create(user=request.user, event=event)
        return redirect('event_home')
    except Event.DoesNotExist:
        return render(request, 'event_not_found.html')


@login_required
def my_booked_events(request):
    current_user = request.user
    events = Event.objects.filter(booked_events__user=current_user)
    return render(request, 'my_booked_events.html', {'events': events})
