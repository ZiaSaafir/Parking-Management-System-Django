from django.shortcuts import render, redirect
from django.contrib import messages

from services.parking_service import ParkingService

from .models import VehicleType


def dashboard(request):

    return render(
        request,
        "dashboard/dashboard.html"
    )


def vehicle_entry(request):

    vehicle_types = VehicleType.objects.all()

    if request.method == "POST":

        vehicle_number = (
            request.POST.get(
                "vehicle_number",
                ""
            )
            .strip()
            .upper()
        )

        vehicle_type_id = request.POST.get(
            "vehicle_type",
            ""
        )

        # Validation

        if not vehicle_number:

            messages.error(
                request,
                "Vehicle number is required."
            )

        elif not vehicle_type_id:

            messages.error(
                request,
                "Vehicle type is required."
            )

        elif not ParkingService.validate_vehicle_number(
            vehicle_number
        ):

            messages.error(
                request,
                "Invalid vehicle number format."
            )

        else:

            try:

                vehicle, created = (
                    ParkingService.register_vehicle(
                        vehicle_number,
                        vehicle_type_id
                    )
                )

                if created:

                    messages.success(
                        request,
                        f"Vehicle {vehicle.vehicle_number} registered successfully."
                    )

                else:

                    messages.warning(
                        request,
                        f"Vehicle {vehicle.vehicle_number} already exists."
                    )

                return redirect(
                    "vehicle_entry"
                )

            except Exception as e:

                messages.error(
                    request,
                    f"Error: {str(e)}"
                )

    context = {
        "vehicle_types": vehicle_types
    }

    return render(
        request,
        "operations/vehicle_entry.html",
        context
    )