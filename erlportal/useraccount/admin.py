from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ErlUser, Profile
from .forms import ErlUserCreationForm, ErlUserChangeForm

# Register your models here.
class ErlUserAdmin(UserAdmin):
    add_form = ErlUserCreationForm
    form = ErlUserChangeForm
    model = ErlUser
    list_display = ['email', 'username']


admin.site.register(ErlUser, ErlUserAdmin)
admin.site.register(Profile)