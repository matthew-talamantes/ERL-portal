from django.db import models

from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
import uuid

# Create your models here.
class ErlUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    def __str__(self):
        return self.username

class Profile(models.Model):
    PHONE = 'phone'
    EMAIL = 'email'
    contactChoices = [(PHONE, 'Phone'), (EMAIL, 'E-Mail')]

    user = models.OneToOneField(ErlUser, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Profile Image', default='default.jpg', upload_to='profile_pics')
    firstName = models.CharField(verbose_name='First Name', max_length=25, blank=False)
    middleName = models.CharField(verbose_name='Middle Name', max_length=25, blank=True)
    lastName = models.CharField(verbose_name='Last Name', max_length=25, blank=False)
    phoneNumber = PhoneNumberField(verbose_name='Phone Number', blank=False)
    shareName = models.BooleanField(verbose_name='Share Name', default=False)
    contactPreference = models.CharField(verbose_name='Contact Preference', max_length=5, choices=contactChoices, default=EMAIL)
    birthDate = models.DateField(verbose_name='Birthday', blank=False)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'slug': self.slug})