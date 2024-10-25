from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from .models import Event, BookedEvent

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(UserChangeForm):
    password = forms.CharField(disabled=True, label="Password", help_text="Unfortunately, you can't update the password.")
    username = forms.CharField(label='username')
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date', 'capacity']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Event Description'}),
            'location': forms.TextInput(attrs={'placeholder': 'Event Location'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DDTHH:MM'}),
            'capacity': forms.NumberInput(attrs={'placeholder': 'Event Capacity'}),
        }
