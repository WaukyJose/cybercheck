# checker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ip_checker_view, name="ip_checker"),
    path("capture/", views.capture_packets, name="capture_packets"),  # <-- añadir esto
]
