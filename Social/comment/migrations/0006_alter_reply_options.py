# Generated by Django 5.1 on 2024-10-04 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0005_alter_reply_parent_post"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reply",
            options={"ordering": ["created"]},
        ),
    ]