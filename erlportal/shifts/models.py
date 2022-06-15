from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

import uuid

from useraccount.models import ErlUser
# Create your models here.

def get_placeholder_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class BaseShift(models.Model):

    REPEAT_CHOICES = [
        (None, 'Do Not Repeat'),
        ('everyday', 'Everyday'),
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdBy = models.ForeignKey(ErlUser, on_delete=models.SET(get_placeholder_user))
    dateCreated = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=25, blank=False)
    description = models.TextField(blank=True)
    startTime = models.DateTimeField(blank=False)
    endTime = models.DateTimeField(blank=False)
    repeat = models.CharField(choices=REPEAT_CHOICES)
    endRepeat = models.DateField(verbose_name='End Repeat', blank=True)
    staffSlots = models.IntegerField(blank=False)
    volSlots = models.IntegerField(blank=False)
    defaultStaff = models.ManyToManyField(ErlUser, related_name='default_staff', blank=True, null=True, on_delete=models.SET_NULL)
    defaultVols = models.ManyToManyField(ErlUser, related_name='default_vols', blank=True, null=True, on_delete=models.SET_NULL)


