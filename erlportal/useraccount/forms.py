from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.models import inlineformset_factory
from django.core.files.uploadedfile import SimpleUploadedFile

from allauth.account.forms import SignupForm

from phonenumber_field.formfields import PhoneNumberField

from PIL import Image

from .models import ErlUser, Profile

class ErlUserCreationForm(UserCreationForm):
    class Meta:
        model = ErlUser
        fields = ('username', 'email')

class ErlUserChangeForm(UserChangeForm):
    class Meta:
        model = ErlUser
        fields = ('username', 'email')

# class ProfileCreateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image', 'firstName', 'middleName', 'lastName', 'phoneNumber',
#             'shareName', 'contactPreference', 'birthDate']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'firstName', 'middleName', 'lastName', 'phoneNumber',
            'shareName', 'contactPreference', 'birthDate']

class ErlSignupForm(SignupForm):

    PHONE = 'phone'
    EMAIL = 'email'
    contactChoices = [(None, ''), (EMAIL, 'E-Mail'), (PHONE, 'Phone')]

    def __init__(self, *args, **kwargs):

        self.imgFile = kwargs.pop('imgFile')
        super().__init__(*args, **kwargs)
        self.fields['firstName'] = forms.CharField(label="First Name", max_length=25, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
        self.fields['middleName'] = forms.CharField(label="Middle Name", max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Middle Name'}), required=False)
        self.fields['lastName'] = forms.CharField(label="Last Name", max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
        self.fields['shareName'] = forms.BooleanField(label="Share Name", required=False)
        self.fields['phoneNumber'] = PhoneNumberField(label='Phone Number', widget=forms.TextInput(attrs={'placeholder': '+17031234567'}))
        self.fields['contactPreference'] = forms.ChoiceField(label='Contact Preference', choices=self.contactChoices)
        self.fields['birthDate'] = forms.DateField(label='Birthdate', input_formats=['%m-%d-%Y'], widget=forms.DateInput(attrs={'placeholder': 'MM-DD-YYYY'}))
        self.fields['image'] = forms.ImageField(label='Profile Image', required=False)
    

    def clean_image(self):
        print('hello')
        print('world')
        # file_data = {'image': SimpleUploadedFile(self.cleaned_data['image'], self.imgFile['image'])}

    def save(self, request):
        user = super().save(request)
        data =self.cleaned_data
        # custom processing here
        profile = Profile(user=user, image=self.imgFile['image'], firstName=data['firstName'], middleName=data['middleName'], lastName=data['lastName'], phoneNumber=data['phoneNumber'], shareName=data['shareName'], contactPreference=data['contactPreference'], birthDate=data['birthDate'])
        profile.save()
        return user

