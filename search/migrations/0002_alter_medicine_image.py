# Generated by Django 5.0.1 on 2024-01-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='medicines/static/search/img'),
        ),
    ]
