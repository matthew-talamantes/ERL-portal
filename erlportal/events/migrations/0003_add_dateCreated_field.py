# Generated by Django 4.0.2 on 2022-02-10 20:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_make_slug_blank'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='dateCreated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
