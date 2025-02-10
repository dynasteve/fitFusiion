from django.db import models
from django.contrib.auth.models import User

class Measurement(models.Model):
    MEASUREMENT_CHOICES = [
        ('upload', 'Upload Images'),
        ('kinect', 'Use Kinect Data'),
        ('manual', 'Input Measurements')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    measurement_type = models.CharField(
    max_length=10,
    choices=[
        ('upload', 'Upload Images'),
        ('kinect', 'Use Kinect Data'),
        ('manual', 'Input Measurements')
    ],
    default='manual'
)

    # Image Upload Fields
    image1 = models.ImageField(upload_to='media/uploads', blank=True, null=True)
    image2 = models.ImageField(upload_to='media/uploads', blank=True, null=True)

    # Manual Measurement Fields
    upper_arm_length = models.FloatField(blank=True, null=True)
    lower_arm_length = models.FloatField(blank=True, null=True)
    upper_leg_length = models.FloatField(blank=True, null=True)
    lower_leg_length = models.FloatField(blank=True, null=True)
    arm_girth = models.FloatField(blank=True, null=True)
    torso_length = models.FloatField(blank=True, null=True)
    shoulder_girth = models.FloatField(blank=True, null=True)
    belly_girth = models.FloatField(blank=True, null=True)

    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Measurement ({self.created_at}) - {self.user.username}"
        
class UploadImage(models.Model):  
    caption = models.CharField(max_length=200)  
    image = models.ImageField(upload_to='images')  
  
    def __str__(self):  
        return f"{self.user.username}'s measurements on {self.created_at}"
