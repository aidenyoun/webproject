# Generated by Django 5.0.1 on 2024-01-15 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage', '0005_alter_medicine_end_date_alter_medicine_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
