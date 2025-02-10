# Generated by Django 5.1.3 on 2025-02-08 15:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='measurements/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='measurements/')),
                ('kinect_data', models.JSONField(blank=True, null=True)),
                ('upper_arm_length', models.FloatField(blank=True, null=True)),
                ('lower_arm_length', models.FloatField(blank=True, null=True)),
                ('upper_leg_length', models.FloatField(blank=True, null=True)),
                ('lower_leg_length', models.FloatField(blank=True, null=True)),
                ('arm_girth', models.FloatField(blank=True, null=True)),
                ('torso_length', models.FloatField(blank=True, null=True)),
                ('shoulder_girth', models.FloatField(blank=True, null=True)),
                ('belly_girth', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_measurements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
