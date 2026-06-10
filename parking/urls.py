from django import views
from django.urls import path

from .views import (
    available_slots_api,
    dashboard,
    vehicle_entry,
    ticket_detail,
    vehicle_exit,
    active_vehicles,
    vehicle_history,
    vehicle_search,
    vehicle_detail_api,
    receipt
)

from .slot_views import (
    parking_slot_create,
    parking_slot_delete,
    parking_slot_list,
    parking_slot_update
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
        "ticket/<int:ticket_id>/",
        ticket_detail,
        name="ticket_detail"
    ),

    path(
        "receipt/<int:ticket_id>/",
        receipt,
        name="receipt"
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
        "slots/",
        parking_slot_list,
        name="parking_slot_list"
    ),
    path(
    "slots/create/",
    parking_slot_create,
    name="parking_slot_create"
),

  path(
    "slots/<int:slot_id>/edit/",
    parking_slot_update,
    name="parking_slot_update"
),

path(
    "slots/<int:slot_id>/delete/",
    parking_slot_delete,
    name="parking_slot_delete"
),
path(
    "api/available-slots/",
    available_slots_api,
    name="available_slots_api"
),
]