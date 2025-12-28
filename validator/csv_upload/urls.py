from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('verify/', views.verify_csv, name='verify_csv'),
]

