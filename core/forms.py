from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Measurement
from django.db import models  
from django.forms import fields  
from .models import UploadImage 

class MeasurementForm(forms.ModelForm):
    image1 = forms.ImageField(required=False)  # Ensure Django processes files
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
        fields = ['measurement_type', 'image1', 'image2', 'upper_arm_length', 
                  'lower_arm_length', 'upper_leg_length', 'lower_leg_length', 
                  'arm_girth', 'torso_length', 'shoulder_girth', 'belly_girth']
                  
class ManualMeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['lower_arm_length', 'upper_leg_length', 'lower_leg_length', 
                  'arm_girth', 'torso_length', 'shoulder_girth', 'belly_girth']

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserImage(forms.ModelForm):  
    class meta:  
        # To specify the model to be used to create form  
        models = UploadImage  
        # It includes all the fields of model  
        fields = '__all__'  
