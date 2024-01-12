# Generated by Django 5.0.1 on 2024-01-11 06:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='medicine_form',
        ),
        migrations.RemoveField(
            model_name='medicine',
            name='medicine_name',
        ),
        migrations.RemoveField(
            model_name='medicine',
            name='notify_time',
        ),
        migrations.AddField(
            model_name='medicine',
            name='dinner_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicine',
            name='form',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='lunch_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicine',
            name='morning_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medicine',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='medicine',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]