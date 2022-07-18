from django import forms

from .models import ShiftInstance

class VolShiftSignupForm(forms.ModelForm):
    class Meta:
        model = ShiftInstance
        fields = []