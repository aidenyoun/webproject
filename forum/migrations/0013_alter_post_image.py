# Generated by Django 5.0.1 on 2024-01-13 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='forum/'),
        ),
    ]