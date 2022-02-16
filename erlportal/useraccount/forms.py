from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ErlUser, Profile

class ErlUserCreationForm(UserCreationForm):
    class Meta:
        model = ErlUser
        fields = ('username', 'email')

class ErlUserChangeForm(UserChangeForm):
    class Meta:
        model = ErlUser
        fields = ('username', 'email')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'firstName', 'middleName', 'lastName', 'phoneNumber',
            'shareName', 'contactPreference', 'birthDate']
