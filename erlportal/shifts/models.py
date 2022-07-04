from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
    date = models.DateField(blank=False)
    startTime = models.TimeField(blank=False)
    endTime = models.TimeField(blank=False)
    repeat = models.CharField(max_length=9, null=True, blank=True, choices=REPEAT_CHOICES)
    endRepeat = models.DateField(verbose_name='End Repeat',null=True, blank=True)
    staffSlots = models.IntegerField(blank=False)
    volSlots = models.IntegerField(blank=False)
    minSlots = models.IntegerField(verbose_name='Minimum Staff/volunteers', blank=False)
    defaultStaff = models.ManyToManyField(ErlUser, related_name='default_staff', blank=True)
    defaultVols = models.ManyToManyField(ErlUser, related_name='default_vols', blank=True)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.endTime <= self.startTime:
            raise ValidationError(_('Must set an end time that is after the start time.'))

        if self.date < timezone.now().date():
            raise ValidationError(_('Must set a date that is equal to or after today\'s date.'))

        if (int(self.staffSlots) + int(self.volSlots)) < int(self.minSlots):
            slotDiff = self.minSlots - (self.staffSlots + self.volSlots)
            self.volSlots += slotDiff
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('base-shift-detail', kwargs={'slug': self.slug})

class ShiftInstance(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    baseShift = models.ForeignKey(BaseShift, on_delete=models.CASCADE)
    date = models.DateField()
    startTime = models.TimeField(blank=True)
    endTime = models.TimeField(blank=True)
    name = models.CharField(max_length=25, blank=True)
    description = models.TextField(blank=True)
    staffSlots = models.IntegerField(blank=True)
    volSlots = models.IntegerField(blank=True)
    minSlots = models.IntegerField(verbose_name='Minimum Staff/volunteers', blank=True)
    staff = models.ManyToManyField(ErlUser, related_name='shift_staff', blank=True)
    vols = models.ManyToManyField(ErlUser, related_name='shift_vols', blank=True)

