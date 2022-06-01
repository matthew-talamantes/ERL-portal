from django.dispatch import receiver
from django.contrib.auth.models import Group

from allauth.account.signals import user_signed_up

from .models import ErlUser

@receiver(user_signed_up, sender=ErlUser)
def add_new_user(sender, **kwargs):
    user = kwargs['user']
    group = Group.objects.get(name='Pending')
    user.groups.add(group)
    user.save()