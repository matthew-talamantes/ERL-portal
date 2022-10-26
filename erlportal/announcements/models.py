from django.db import models
from django.utils import timezone

# Create your models here.

class Announcement(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(default='', blank=True)
    dateCreated = models.DateTimeField(default=timezone.now, editable=False)
    
