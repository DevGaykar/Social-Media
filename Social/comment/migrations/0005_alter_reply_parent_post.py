# Generated by Django 5.1 on 2024-10-04 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0004_reply"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reply",
            name="parent_post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="comment.comment",
            ),
        ),
    ]