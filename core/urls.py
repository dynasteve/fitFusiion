from django.urls import path
from . import views
from .views import measurement_detail
from django.conf import settings
from django.conf.urls.static import static
from core.views import list_new_images, upload_result
from core.views import image_request, upload_image
  
# app_name = 'sampleapp'  

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('measurements/new/', views.new_measurement, name='new_measurement'),  # ? This is important!
    path("loading_screen/", views.loading_screen, name="loading_screen"),
    path('measurements/delete/<int:measurement_id>/', views.delete_measurement, name='delete_measurement'),
    path('measurements/<int:measurement_id>/', measurement_detail, name='measurement_detail'),
    path("measurements/", views.measurements_list, name="measurements_list"),
    path("api/new_images/", list_new_images, name="list_new_images"),
    path("api/upload_result/", upload_result, name="upload_result"),
    path("api/upload_image/", upload_image, name="upload_image"),
    path('', image_request, name = "image-request"),
] 

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
