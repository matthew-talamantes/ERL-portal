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
    startTime = models.DateTimeField(blank=False)
    endTime = models.DateTimeField(blank=False)
    repeat = models.CharField(choices=REPEAT_CHOICES)
    endRepeat = models.DateField(verbose_name='End Repeat', blank=True)
    staffSlots = models.IntegerField(blank=False)
    volSlots = models.IntegerField(blank=False)
    minSlots = models.IntegerField(verbose_name='Minimum Staff/volunteers', blank=False)
    defaultStaff = models.ManyToManyField(ErlUser, related_name='default_staff', blank=True, null=True, on_delete=models.SET_NULL)
    defaultVols = models.ManyToManyField(ErlUser, related_name='default_vols', blank=True, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.endTime <= self.startTime:
            raise ValidationError(_('Must set an end time that is after the start time.'))

        if (int(self.staffSlots) + int(self.volSlots)) < int(self.minSlots):
            slotDiff = self.minSlots - (self.staffSlots + self.volSlots)
            self.volSlots += slotDiff
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('base-shift-detail', kwargs={'slug': self.slug})


