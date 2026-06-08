from django.urls import path

from .views import (
    active_vehicles,
    dashboard,
    receipt,
    vehicle_detail_api,
    vehicle_entry,
    ticket_detail,
    vehicle_exit,
    vehicle_history,
    vehicle_search
)
urlpatterns = [

    path(
        "",
        dashboard,
        name="dashboard"
    ),

    path(
        "entry/",
        vehicle_entry,
        name="vehicle_entry"
    ),

    path(
        "ticket/<int:ticket_id>/",
        ticket_detail,
        name="ticket_detail"
    ),
    path(
    "exit/",
    vehicle_exit,
    name="vehicle_exit"
),
path(
    "active-vehicles/",
    active_vehicles,
    name="active_vehicles"
),
path(
    "vehicle-history/",
    vehicle_history,
    name="vehicle_history"
),
 path(
        "search-vehicle/",
        vehicle_search,
        name="vehicle_search"
    ),
    path(
    "vehicle/<int:vehicle_id>/",
    vehicle_detail_api,
    name="vehicle_detail_api"
),
path(
    "receipt/<int:ticket_id>/",
    receipt,
    name="receipt"
),
]