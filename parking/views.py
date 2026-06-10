from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum

from services.permissions import role_required
from services.parking_service import ParkingService
from services.slot_service import SlotService

from .models import (
    Vehicle,
    VehicleType,
    ParkingSlot,
    ParkingTicket,
    Payment
)


@login_required
def dashboard(request):

    context = {
        "total_slots": ParkingSlot.objects.count(),
        "free_slots": ParkingSlot.objects.filter(status="FREE").count(),
        "occupied_slots": ParkingSlot.objects.filter(status="OCCUPIED").count(),
        "active_tickets": ParkingTicket.objects.filter(status="ACTIVE").count(),
        "completed_tickets": ParkingTicket.objects.filter(status="COMPLETED").count(),
        "total_revenue": (
            Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
        ),
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


@login_required
@role_required("ADMIN", "OPERATOR")
def vehicle_entry(request):

    vehicle_types = VehicleType.objects.all()

    free_slots = SlotService.get_free_slots()

    suggested_slot = SlotService.get_free_slot()

    if request.method == "POST":

        vehicle_number = (
            request.POST.get("vehicle_number", "")
            .strip()
            .upper()
        )

        owner_name = (
            request.POST.get("owner_name", "")
            .strip()
        )

        owner_phone = (
            request.POST.get("owner_phone", "")
            .strip()
        )

        vehicle_type_id = request.POST.get(
            "vehicle_type",
            ""
        )

        slot_id = request.POST.get(
            "slot",
            ""
        )

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
                "Invalid vehicle number."
            )

        else:

            try:

                vehicle, created = ParkingService.register_vehicle(
                    vehicle_number,
                    vehicle_type_id,
                    owner_name,
                    owner_phone
                )

                ticket = ParkingService.create_ticket(
                    vehicle,
                    slot_id
                )

                messages.success(
                    request,
                    "Parking ticket created successfully."
                )

                return redirect(
                    "ticket_detail",
                    ticket_id=ticket.id
                )

            except Exception as e:

                messages.error(
                    request,
                    str(e)
                )

    context = {
        "vehicle_types": vehicle_types,
        "free_slots": free_slots,
        "suggested_slot": suggested_slot,
    }

    return render(
        request,
        "operations/vehicle_entry.html",
        context
    )


@login_required
@role_required("ADMIN", "OPERATOR")
def ticket_detail(request, ticket_id):

    ticket = get_object_or_404(
        ParkingTicket,
        id=ticket_id
    )

    context = {
        "ticket": ticket
    }

    return render(
        request,
        "operations/ticket_detail.html",
        context
    )


@login_required
@role_required("ADMIN", "OPERATOR")
def vehicle_exit(request):

    if request.method == "POST":

        try:

            vehicle_number = (
                request.POST.get("vehicle_number", "")
                .strip()
                .upper()
            )

            payment_method = request.POST.get(
                "payment_method",
                "CASH"
            )

            payment = ParkingService.process_exit(
                vehicle_number,
                payment_method
            )

            messages.success(
                request,
                "Vehicle exited successfully."
            )

            return redirect(
                "receipt",
                ticket_id=payment.ticket.id
            )

        except Exception as e:

            messages.error(
                request,
                str(e)
            )

    return render(
        request,
        "operations/vehicle_exit.html"
    )


@login_required
@role_required("ADMIN", "OPERATOR")
def active_vehicles(request):

    tickets = (
        ParkingTicket.objects
        .filter(status="ACTIVE")
        .select_related(
            "vehicle",
            "vehicle__vehicle_type",
            "slot"
        )
        .order_by("-entry_time")
    )

    context = {
        "tickets": tickets
    }

    return render(
        request,
        "operations/active_vehicles.html",
        context
    )


@login_required
@role_required("ADMIN", "OPERATOR")
def vehicle_history(request):

    vehicles = (
        Vehicle.objects
        .select_related("vehicle_type")
        .order_by("-total_visits")
    )

    context = {
        "vehicles": vehicles
    }

    return render(
        request,
        "reports/vehicle_history.html",
        context
    )


@login_required
@role_required("ADMIN", "OPERATOR")
def vehicle_search(request):

    query = (
        request.GET.get("q", "")
        .strip()
        .upper()
    )

    vehicles = (
        Vehicle.objects
        .filter(vehicle_number__icontains=query)[:10]
    )

    data = []

    for vehicle in vehicles:

        data.append({
            "id": vehicle.id,
            "vehicle_number": vehicle.vehicle_number,
            "owner_name": vehicle.owner_name,
            "owner_phone": vehicle.owner_phone,
            "total_visits": vehicle.total_visits,
            "vehicle_type": vehicle.vehicle_type.name,
        })

    return JsonResponse(
        data,
        safe=False
    )


@login_required
@role_required("ADMIN", "OPERATOR")
def vehicle_detail_api(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id
    )

    data = {
        "id": vehicle.id,
        "vehicle_number": vehicle.vehicle_number,
        "owner_name": vehicle.owner_name,
        "owner_phone": vehicle.owner_phone,
        "vehicle_type_id": vehicle.vehicle_type.id,
        "vehicle_type": vehicle.vehicle_type.name,
        "total_visits": vehicle.total_visits,
        "last_visit": (
            vehicle.last_visit.strftime("%Y-%m-%d %H:%M")
            if vehicle.last_visit
            else ""
        )
    }

    return JsonResponse(data)


@login_required
@role_required("ADMIN", "OPERATOR")
def receipt(request, ticket_id):

    ticket = get_object_or_404(
        ParkingTicket,
        id=ticket_id
    )

    payment = (
        Payment.objects
        .filter(ticket=ticket)
        .first()
    )

    context = {
        "ticket": ticket,
        "payment": payment
    }

    return render(
        request,
        "payments/receipt.html",
        context
    )


@login_required
@role_required(
    "ADMIN",
    "OPERATOR"
)
def available_slots_api(
    request
):
    """
    Return compatible free slots.
    """

    vehicle_type = request.GET.get(
        "vehicle_type",
        ""
    )

    slots = (
        SlotService.get_compatible_free_slots(
            vehicle_type
        )
    )

    data = []

    for slot in slots:

        data.append({
            "id": slot.id,
            "slot_number": slot.slot_number,
            "slot_type": slot.slot_type,
        })

    return JsonResponse(
        data,
        safe=False
    )