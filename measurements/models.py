from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="measurements_measurements")
    date = models.DateTimeField(auto_now_add=True)
    upper_arm_length = models.FloatField(null=True, blank=True)
    lower_arm_length = models.FloatField(null=True, blank=True)
    upper_leg_length = models.FloatField(null=True, blank=True)
    lower_leg_length = models.FloatField(null=True, blank=True)
    arm_girth = models.FloatField(null=True, blank=True)
    torso_length = models.FloatField(null=True, blank=True)
    shoulder_girth = models.FloatField(null=True, blank=True)
    belly_girth = models.FloatField(null=True, blank=True)
    image1 = models.ImageField(upload_to='measurements/', null=True, blank=True)
    image2 = models.ImageField(upload_to='measurements/', null=True, blank=True)

    def __str__(self):
        return f"Measurement {self.date} - {self.user.username}"
