import json
import re
import os
import imghdr
import base64
import time
import shutil

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .forms import MeasurementForm
from .models import Measurement
from django.shortcuts import get_object_or_404

from django.http import JsonResponse

from django.conf import settings
  
from django.conf.urls.static import static  

from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import UploadImage  
from .forms import UploadMeasurementForm, ManualMeasurementForm

from django.shortcuts import redirect
from django.contrib.auth import logout


@login_required
def home(request):
    clear_media_folders()
    measurements = Measurement.objects.filter(user=request.user).order_by('-created_at')
    print("Retrieved measurements:", measurements)  # Debugging
    return render(request, 'core/home.html', {'measurements': measurements})

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print("?? Received POST data:", request.POST)  # Debugging

        if form.is_valid():
            user = form.save()
            print("? User Created:", user)  # Debugging

            login(request, user)  # Log in the new user
            messages.success(request, "Account created successfully!")  # Flash message
            return redirect('home')  # Redirect to home

        else:
            print("? Form Errors:", form.errors)  # Debugging
            messages.error(request, "There was an error with your submission.")  

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
    

@login_required
def new_measurement(request):
    return render(request, "core/new_measurement.html")

@login_required
def upload_measurement(request):
    if request.method == "POST":
        print("?? Received POST request:", request.POST)
        print("?? Received FILES:", request.FILES)

        measurement = Measurement(user=request.user, measurement_type="upload")

        def fix_filename(file, new_name):
            """Rename uploaded file to a fixed name (front/side) while keeping its extension."""
            if "." not in file.name:
                detected_type = imghdr.what(file)  # Detect image type
                extension = detected_type if detected_type else "jpg"  # Default to .jpg
            else:
                extension = file.name.split(".")[-1]  # Keep the original extension

            return f"{new_name}.{extension}"

        # ? Process image1 (rename to "front.ext")
        if "image1" in request.FILES:
            image1 = request.FILES["image1"]
            new_name1 = fix_filename(image1, "front")

            # Save image to media/uploads/
            save_path1 = os.path.join("uploads", new_name1)  # ? Use relative path
            default_storage.save(save_path1, ContentFile(image1.read()))

            # Store in database
            measurement.image1.name = save_path1
            measurement.image1_data = image1.read()  # Save as binary
            print(f"? Image 1 saved: {new_name1}")

        # ? Process image2 (rename to "side.ext")
        if "image2" in request.FILES:
            image2 = request.FILES["image2"]
            new_name2 = fix_filename(image2, "side")

            # Save image to media/uploads/
            save_path2 = os.path.join("uploads", new_name2)  # ? Use relative path
            default_storage.save(save_path2, ContentFile(image2.read()))

            # Store in database
            measurement.image2.name = save_path2
            measurement.image2_data = image2.read()  # Save as binary
            print(f"? Image 2 saved: {new_name2}")

        measurement.save()
        print("? Measurement saved successfully!")

        return redirect("loading_screen")

    return render(request, "core/upload_measurement.html")

@login_required
def manual_measurement(request):
    if request.method == "POST":
        form = ManualMeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user  # ? Assign logged-in user
            measurement.measurement_type = "manual"
            measurement.save()
            return redirect("loading_screen")
        else:
            print("? Form errors:", form.errors)  # Debugging
    else:
        form = ManualMeasurementForm()

    return render(request, "core/manual_measurement.html", {"form": form})


@login_required
def kinect_measurement(request):
    if request.method == "POST":
        # Kinect logic here (if needed)
        return redirect("loading_screen")

    return render(request, "core/kinect_measurement.html")


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
        if "image1" not in request.FILES and "image2" not in request.FILES:
            return JsonResponse({"error": "No images uploaded"}, status=400)

        measurement = Measurement(user=request.user, measurement_type="upload")

        if "image1" in request.FILES:
            measurement.image1 = request.FILES["image1"]

        if "image2" in request.FILES:
            measurement.image2 = request.FILES["image2"]

        measurement.save()  # ? Now saving to DB

        return JsonResponse({"message": "Images uploaded successfully", "id": measurement.id})


    
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
    
#@login_required
#def upload_measurements(request):
#    if request.method == 'POST':
#        form = ManualMeasurementForm(request.POST)
#        if form.is_valid():
#            measurement = form.save(commit=False)
#            measurement.user = request.user
#            measurement.save()
#            return redirect('home')
#    else:
#        form = ManualMeasurementForm()
#    return render(request, 'core/new_measurements.html', {'form': form})
    
@login_required
def view_measurements(request):
    measurements = Measurement.objects.filter(user=request.user)
    return render(request, 'core/measurement_detail.html', {'measurements': measurements})
    
def check_results(request, measurement_id):
    """Check if the output files exist in media/results/"""
    measurement = get_object_or_404(Measurement, id=measurement_id)

    results_dir = os.path.join(settings.MEDIA_ROOT, "results")
    expected_json = os.path.join(results_dir, f"{measurement_id}.json")
    expected_images = [os.path.join(results_dir, f"{measurement_id}_1.jpg"),
                       os.path.join(results_dir, f"{measurement_id}_2.jpg")]

    # Kinect mode only expects a JSON file, Upload mode expects both JSON & images
    if measurement.measurement_type == "kinect":
        if os.path.exists(expected_json):
            return JsonResponse({"status": "ready"})
    elif measurement.measurement_type == "upload":
        if os.path.exists(expected_json) and all(os.path.exists(img) for img in expected_images):
            return JsonResponse({"status": "ready"})

    return JsonResponse({"status": "pending"})
    
    
def process_json_measurement(request, measurement_id):
    """Reads a JSON file from media/results/ and updates the measurement."""
    measurement = Measurement.objects.get(id=measurement_id)

    json_path = os.path.join(settings.MEDIA_ROOT, "results", f"{measurement_id}.json")

    if os.path.exists(json_path):
        with open(json_path, "r") as file:
            data = json.load(file)
        
        # Update measurement fields
        measurement.chest_girth = data.get("Chest Girth")
        measurement.hips_girth = data.get("Hips Girth")
        measurement.waist_girth = data.get("Waist Girth")
        measurement.thigh_girth = data.get("Thigh Girth")
        measurement.neck_size = data.get("Neck Size")
        measurement.upper_arm_girth = data.get("Upper Arm Girth")
        measurement.calves_girth = data.get("Calves Girth")
        measurement.upper_arm_length = data.get("Upper Arm Length")
        measurement.lower_arm_length = data.get("Lower Arm Length")
        measurement.upper_leg_length = data.get("Upper Leg Length")
        measurement.lower_leg_length = data.get("Lower Leg Length")
        measurement.torso_length = data.get("Torso Length")

        measurement.save()
        return True
    return False


def check_results(request):
    results_dir = os.path.join(settings.MEDIA_ROOT, "results")
    found = any(f.endswith(".txt") for f in os.listdir(results_dir))  # Look for .txt files
    return JsonResponse({"found": found})
    
def check_kinect_result(request):
    """Check if result.txt exists in media/results."""
    result_path = os.path.join(settings.MEDIA_ROOT, "results", "result.txt")
    
    print(f"?? Checking for file: {result_path}")  # Debugging: Check the exact path

    if os.path.exists(result_path):
        print("? File found!")  # Debugging: File is detected

        result = process_kinect_results(request)  # Process the file

        if "error" in result:
            print(f"? Error: {result['error']}")  # Debugging: Show error
            return JsonResponse({"status": "error", "message": result["error"]})

        print("? Kinect results saved!")  # Debugging: Success
        return JsonResponse({"status": "done", "message": "Kinect results saved", "id": result["id"]})
    
    print("? Still waiting for Kinect results...")  # Debugging: File is missing
    return JsonResponse({"status": "waiting", "message": "Still waiting for Kinect results"})

    
@csrf_exempt  # Allows the request from an external device
def upload_kinect_result(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        file_path = os.path.join(settings.MEDIA_ROOT, "results", file.name)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        return JsonResponse({"message": "Kinect file uploaded successfully", "path": file_path})
    
    return JsonResponse({"error": "No file received"}, status=400)
    
def process_kinect_results(request):
    """Read the uploaded Kinect result.txt and save measurements to the database."""
    result_path = os.path.join(settings.MEDIA_ROOT, "results", "result.txt")

    if not os.path.exists(result_path):
        return {"error": "No Kinect results found."}

    try:
        with open(result_path, "r") as file:
            lines = file.readlines()

        measurement_data = {}
        pattern = r"([\w\s]+):\s([\d.]+)\smm"

        for line in lines:
            match = re.match(pattern, line)
            if match:
                key = match.group(1).strip().lower().replace(" ", "_")  # Convert to snake_case
                value = float(match.group(2))  # Convert string to float
                measurement_data[key] = value

        # Required fields check
        required_fields = {
            "chest_girth", "hips_girth", "waist_girth", "thigh_girth",
            "neck_size", "upper_arm_girth", "calves_girth", "upper_arm_length",
            "lower_arm_length", "upper_leg_length", "lower_leg_length", "torso_length"
        }

        if not required_fields.issubset(set(measurement_data.keys())):
            return {"error": "Missing measurement fields in result.txt"}

        # Save to the database
        print(f"?? Current User: {request.user}")
        measurement = Measurement.objects.create(
            user=request.user,  # Update this to the correct user if necessary
            measurement_type="kinect",
            chest_girth=measurement_data["chest_girth"],
            hips_girth=measurement_data["hips_girth"],
            waist_girth=measurement_data["waist_girth"],
            thigh_girth=measurement_data["thigh_girth"],
            neck_size=measurement_data["neck_size"],
            upper_arm_girth=measurement_data["upper_arm_girth"],
            calves_girth=measurement_data["calves_girth"],
            upper_arm_length=measurement_data["upper_arm_length"],
            lower_arm_length=measurement_data["lower_arm_length"],
            upper_leg_length=measurement_data["upper_leg_length"],
            lower_leg_length=measurement_data["lower_leg_length"],
            torso_length=measurement_data["torso_length"],
        )

        return {"status": "success", "id": measurement.id}

    except Exception as e:
        return {"error": str(e)}

def clear_media_folders():
    """Deletes all files in media/upload/ and media/results/ on server startup."""
    media_dirs = ["media/uploads", "media/results"]

    for directory in media_dirs:
        dir_path = os.path.join(settings.BASE_DIR, directory)
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
