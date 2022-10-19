from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.core.files.images import ImageFile

from allauth.account.forms import SignupForm

from phonenumber_field.formfields import PhoneNumberField

from PIL import Image
import os

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

    def clean_image(self):
        uploaded_image = self.cleaned_data.get('image')
        if not uploaded_image:
            imgFile = open(settings.MEDIA_ROOT / 'default.jpg', 'rb')
            uploaded_image = ImageFile(imgFile, name='default.jpg')

        return uploaded_image
        
    class Meta:
        model = Profile
        fields = ['image', 'firstName', 'middleName', 'lastName', 'phoneNumber',
            'shareName', 'contactPreference', 'birthDate']

class ErlSignupForm(SignupForm):

    PHONE = 'phone'
    EMAIL = 'email'
    contactChoices = [(EMAIL, 'E-Mail'), (PHONE, 'Phone')]

    def __init__(self, *args, **kwargs):
        if args:
            data = args[0]
        else:
            data = kwargs.get('data', None)
        if data:
            data = data.copy()
            phoneNum = data['phoneNumber']
            if len(phoneNum) < 12 and phoneNum[0:2] != '+1':
                phoneNum = '+1' + phoneNum
                data['phoneNumber'] = phoneNum
                kwargs['data'] = data
        self.imgFile = kwargs.pop('imgFile')
        super().__init__(*args, **kwargs)
        self.fields['firstName'] = forms.CharField(label="First Name", max_length=25, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
        self.fields['middleName'] = forms.CharField(label="Middle Name", max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Middle Name'}), required=False)
        self.fields['lastName'] = forms.CharField(label="Last Name", max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
        self.fields['shareName'] = forms.BooleanField(label="Share Name", required=False)
        self.fields['phoneNumber'] = PhoneNumberField(label='Phone Number')
        self.fields['contactPreference'] = forms.ChoiceField(label='Contact Preference', choices=self.contactChoices, widget=forms.RadioSelect())
        self.fields['birthDate'] = forms.DateField(label='Birthdate', input_formats=['%Y-%m-%d'], widget=forms.DateInput(attrs={'placeholder': 'MM-DD-YYYY', 'type': 'date'}))
        self.fields['image'] = forms.ImageField(label='Profile Image', required=False)

    def save(self, request):
        user = super().save(request)
        # Custom processing here
        data = self.cleaned_data

        if data['image'] == None:
            profile = Profile(user=user, firstName=data['firstName'], middleName=data['middleName'], lastName=data['lastName'], phoneNumber=data['phoneNumber'], shareName=data['shareName'], contactPreference=data['contactPreference'], birthDate=data['birthDate'])
        else:
            profile = Profile(user=user, image=self.imgFile['image'], firstName=data['firstName'], middleName=data['middleName'], lastName=data['lastName'], phoneNumber=data['phoneNumber'], shareName=data['shareName'], contactPreference=data['contactPreference'], birthDate=data['birthDate'])
        
        try:
            profile.save()
            return user
        except:
            print('An errror occured')

class ApproveUserForm(forms.Form):

    userName = forms.CharField(widget=forms.HiddenInput)
    def approve_user(self, name):
        user = ErlUser.objects.get(username=name)
        volGroup = Group.objects.get(name='Volunteer')
        pendGroup = Group.objects.get(name='Pending')
        user.groups.add(volGroup)
        user.groups.remove(pendGroup)
        user.save()

    def reject_user(self, name):
        user = ErlUser.objects.get(username=name)
        pendGroup = Group.objects.get(name='Pending')
        user.groups.remove(pendGroup)
        user.is_active = False
        user.save()
            
        

