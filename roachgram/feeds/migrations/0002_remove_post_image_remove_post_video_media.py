# Generated by Django 5.0.2 on 2024-02-23 13:13

import django.db.models.deletion
import feeds.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='video',
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(blank=True, null=True, upload_to=feeds.models.mediaDirectory)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_media', to='feeds.post')),
            ],
        ),
    ]
