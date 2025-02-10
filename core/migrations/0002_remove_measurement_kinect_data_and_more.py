# Generated by Django 5.1.3 on 2025-02-08 17:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='kinect_data',
        ),
        migrations.AddField(
            model_name='measurement',
            name='measurement_type',
            field=models.CharField(choices=[('upload', 'Upload Images'), ('kinect', 'Use Kinect Data'), ('manual', 'Input Measurements')], default='manual', max_length=10),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
