# Generated by Django 4.1.7 on 2023-03-28 22:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('room', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
