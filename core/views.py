import json
import os

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .forms import MeasurementForm
from .forms import ManualMeasurementForm
from .models import Measurement
from django.shortcuts import get_object_or_404

from django.http import JsonResponse

from django.conf import settings
  
from django.conf.urls.static import static  

from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .forms import UserImage
from .models import UploadImage  



@login_required
def home(request):
    measurements = Measurement.objects.filter(user=request.user).order_by('-created_at')
    print("Retrieved measurements:", measurements)  # Debugging
    return render(request, 'core/home.html', {'measurements': measurements})

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('home')
    else:
        form = SignupForm()
    
    return render(request, 'core/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')
    
@login_required
def new_measurement(request):
    if request.method == "POST":
        form = MeasurementForm(request.POST, request.FILES)  # Include request.FILES

        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user  # Assign the user
            measurement.image1 = form.cleaned_data["image1"]
            measurement.image2 = form.cleaned_data["image2"]
            measurement.save()  # Save with images

            return redirect("loading_screen")

    else:
        form = MeasurementForm()

    return render(request, "core/new_measurement.html", {"form": form})


@login_required
def delete_measurement(request, measurement_id):
    measurement = get_object_or_404(Measurement, id=measurement_id, user=request.user)
    measurement.delete()
    return redirect('home')

@login_required
def loading_screen(request):
    return render(request, 'core/loading.html')

@login_required
def measurement_detail(request, measurement_id):
    measurement = Measurement.objects.filter(user=request.user)
    measurement = get_object_or_404(Measurement, id=measurement_id, user=request.user)
    return render(request, 'core/measurement_detail.html', {'measurement': measurement})

@login_required
def save_measurement(request):
    if request.method == "POST":
        print("Received POST data:", request.POST)  # Debugging
        try:
            data = json.loads(request.body)  # Ensure JSON is correctly parsed
            measurement_data = data.get("measurements", {})  # Extract JSON data

            # Save the measurement with proper JSON formatting
            measurement = Measurement.objects.create(
                user=request.user,
                measurement_type=data.get("type", "manual"),
                data=measurement_data  # Ensure this is storing JSON correctly
            )

            return JsonResponse({'message': 'Measurement saved', 'id': measurement.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            

@login_required
def view_measurements(request):
    measurements = Measurement.objects.filter(user=request.user)
    return render(request, 'core/measurement_detail.html', {'measurements': measurements})
            

def submit_measurements(request):
    if request.method == "POST":
        print("Raw request body:", request.body)  # Debugging line
        print("POST data:", request.POST)  # Debugging line

        try:
            data = json.loads(request.body)  # Ensure JSON parsing
            print("Parsed data:", data)  # Debugging line
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
            
def measurements_list(request):
    measurements = Measurement.objects.filter(user=request.user)
    return render(request, "core/list.html", {"measurements": measurements})

# API to list uploaded images
def list_new_images(request):
    images_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    images = [f for f in os.listdir(images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_urls = [request.build_absolute_uri(settings.MEDIA_URL + "uploads/" + img) for img in images]
    return JsonResponse({"images": image_urls})

# API to receive processed images
@csrf_exempt
def upload_result(request):
    if request.method == "POST" and request.FILES.get("result"):
        file = request.FILES["result"]
        path = default_storage.save("results/" + file.name, ContentFile(file.read()))
        return JsonResponse({"message": "File uploaded successfully", "path": path})
    return JsonResponse({"error": "No file received"}, status=400)
    
@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        print("FILES RECEIVED:", request.FILES)  # Debugging

        if "image1" not in request.FILES and "image2" not in request.FILES:
            return JsonResponse({"error": "No images uploaded"}, status=400)

        upload_folder = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_folder, exist_ok=True)  # Ensure the folder exists

        saved_files = []

        # Handle image1
        if "image1" in request.FILES:
            image1 = request.FILES["image1"]
            file_path1 = os.path.join(upload_folder, image1.name)
            with open(file_path1, "wb") as destination:
                for chunk in image1.chunks():
                    destination.write(chunk)
            saved_files.append(file_path1)

        # Handle image2
        if "image2" in request.FILES:
            image2 = request.FILES["image2"]
            file_path2 = os.path.join(upload_folder, image2.name)
            with open(file_path2, "wb") as destination:
                for chunk in image2.chunks():
                    destination.write(chunk)
            saved_files.append(file_path2)

        return JsonResponse({"message": "Images uploaded successfully", "files": saved_files})

    
def image_request(request):  
    if request.method == 'POST':  
        form = UserImageForm(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
  
            # Getting the current instance object to display in the template  
            img_object = form.instance  
              
            return render(request, 'image_form.html', {'form': form, 'img_obj': img_object})  
    else:  
        form = UserImageForm()  
  
    return render(request, 'image_form.html', {'form': form})
    
@login_required
def upload_measurements(request):
    if request.method == 'POST':
        form = ManualMeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            return redirect('home')
    else:
        form = ManualMeasurementForm()
    return render(request, 'core/new_measurements.html', {'form': form})
    
@login_required
def view_measurements(request):
    measurements = Measurement.objects.filter(user=request.user)
    return render(request, 'core/measurement_detail.html', {'measurements': measurements})

