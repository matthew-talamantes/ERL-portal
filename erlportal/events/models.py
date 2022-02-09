from django.db import models
import uuid
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.utils import IntegrityError
from django.db import transaction

# Create your models here.
class Event(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50, blank=False)
    eventType = models.CharField(verbose_name='type', max_length=5, default='event', editable=False)
    year = models.CharField(max_length=4, blank=False)
    month = models.CharField(max_length=2, blank=False)
    day = models.CharField(max_length=2, blank=False)
    startTime = models.CharField(max_length=5, blank=False)
    endTime = models.CharField(max_length=5, blank=False)
    description = models.TextField()
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if Event.objects.filter(slug=self.slug).exists():
            validSlug = False
            count = 1
            while not validSlug:
                self.slug += f'-{count}'
                if Event.objects.filter(slug=self.slug).exists():
                    count += 1
                else:
                    validSlug = True
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event', kwargs={'slug': self.slug})
