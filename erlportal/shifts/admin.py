from django.contrib import admin

from .models import BaseShift, ShiftInstance

# Register your models here.
admin.site.register(BaseShift)
admin.site.register(ShiftInstance)