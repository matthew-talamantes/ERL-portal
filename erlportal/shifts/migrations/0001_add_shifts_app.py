# Generated by Django 4.0.4 on 2022-06-17 21:20

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone
import shifts.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseShift',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(blank=True)),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('repeat', models.CharField(choices=[(None, 'Do Not Repeat'), ('everyday', 'Everyday'), ('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday')], max_length=9)),
                ('endRepeat', models.DateField(blank=True, verbose_name='End Repeat')),
                ('staffSlots', models.IntegerField()),
                ('volSlots', models.IntegerField()),
                ('minSlots', models.IntegerField(verbose_name='Minimum Staff/volunteers')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('createdBy', models.ForeignKey(on_delete=models.SET(shifts.models.get_placeholder_user), to=settings.AUTH_USER_MODEL)),
                ('defaultStaff', models.ManyToManyField(blank=True, related_name='default_staff', to=settings.AUTH_USER_MODEL)),
                ('defaultVols', models.ManyToManyField(blank=True, related_name='default_vols', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
