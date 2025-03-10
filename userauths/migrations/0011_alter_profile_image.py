# Generated by Django 5.1.3 on 2025-01-04 19:27

import cloudinary_storage.storage
import django_resized.forms
import userauths.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("userauths", "0010_alter_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format=None,
                keep_meta=True,
                null=True,
                quality=85,
                scale=None,
                size=[600, 600],
                storage=cloudinary_storage.storage.MediaCloudinaryStorage(),
                upload_to=userauths.models.profile_picture_path,
            ),
        ),
    ]
