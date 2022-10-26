from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField

from useraccount.models import ErlUser
from events.models import Event

# Create your models here.

class Announcement(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = RichTextField(default='', blank=True)
    dateCreated = models.DateTimeField(default=timezone.now, editable=False)
    postedBy = models.ForeignKey(ErlUser, on_delete=models.CASCADE)
    viewPerms = models.CharField(verbose_name='Who can see this announcement', max_length=10, choices=Event.VIEW_PERMS, default='volunteers', blank=False, null=False)

