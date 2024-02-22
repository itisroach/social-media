# Generated by Django 5.0.2 on 2024-02-22 18:24

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='followuser',
            name='createdAt',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='followuser',
            name='updatedAt',
            field=models.TimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, default='default-profile.png', null=True, upload_to=users.models.user_profile_directory),
        ),
    ]
