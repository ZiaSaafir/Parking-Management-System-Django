from django.urls import path
from .views import dashboard, vehicle_entry

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("entry/", vehicle_entry, name="vehicle-entry"),
]