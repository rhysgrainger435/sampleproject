# Generated by Django 4.1.7 on 2023-04-06 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile_age_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interest',
            field=models.TextField(blank=True, max_length=250),
        ),
    ]