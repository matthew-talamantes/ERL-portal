# Generated by Django 4.0.4 on 2022-07-04 19:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0003_make_repeat_nullable_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseshift',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='baseshift',
            name='endTime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='baseshift',
            name='startTime',
            field=models.TimeField(),
        ),
    ]