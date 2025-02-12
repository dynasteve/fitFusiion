from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Measurement
from django.db import models  
from django.forms import fields  
from .models import UploadImage 
from django.core.validators import FileExtensionValidator

class MeasurementForm(forms.ModelForm):
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)

    MEASUREMENT_CHOICES = [
        ('upload', 'Upload Images'),
        ('kinect', 'Use Kinect Data'),
        ('manual', 'Input Measurements')
    ]

    measurement_type = forms.ChoiceField(
        choices=MEASUREMENT_CHOICES, widget=forms.RadioSelect, required=True
    )

    class Meta:
        model = Measurement
        fields = [
            'measurement_type', 'image1', 'image2', 
            'chest_girth', 'hips_girth', 'waist_girth', 'thigh_girth',
            'neck_size', 'upper_arm_girth', 'calves_girth', 'upper_arm_length',
            'lower_arm_length', 'upper_leg_length', 'lower_leg_length', 'torso_length'
        ]
                  
class ManualMeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = [
            'chest_girth', 'hips_girth', 'waist_girth', 'thigh_girth',
            'neck_size', 'upper_arm_girth', 'calves_girth', 'upper_arm_length',
            'lower_arm_length', 'upper_leg_length', 'lower_leg_length', 'torso_length'
        ]

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserImageForm(forms.ModelForm):  # Fix class name
    class Meta:
        model = UploadImage  # Fix 'models' ? 'model'
        fields = '__all__'
        

class UploadMeasurementForm(forms.ModelForm):
    image1 = forms.ImageField(
        required=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp'])]
    )
    image2 = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp'])]
    )

    class Meta:
        model = Measurement
        fields = ['image1', 'image2']
