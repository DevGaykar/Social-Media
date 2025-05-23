# Generated by Django 5.1.3 on 2025-02-23 13:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0002_storyview'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Stories'},
        ),
        migrations.RenameField(
            model_name='storyview',
            old_name='user',
            new_name='viewer',
        ),
        migrations.AlterUniqueTogether(
            name='storyview',
            unique_together={('story', 'viewer')},
        ),
    ]
