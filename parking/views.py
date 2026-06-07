from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import Vehicle,ParkingTicket
from django.contrib import messages

from services.parking_service import (
    ParkingService
)
from services.slot_service import (
    SlotService
)

from services.payment_service import (
    PaymentService
)


from .models import (
    VehicleType,
    ParkingTicket
)

from django.db.models import Sum

from .models import (
    ParkingSlot,
    ParkingTicket,
    Payment
)

def dashboard(request):

    total_slots = (
        ParkingSlot.objects.count()
    )

    free_slots = (
        ParkingSlot.objects.filter(
            status="FREE"
        ).count()
    )

    occupied_slots = (
        ParkingSlot.objects.filter(
            status="OCCUPIED"
        ).count()
    )

    active_tickets = (
        ParkingTicket.objects.filter(
            status="ACTIVE"
        ).count()
    )

    completed_tickets = (
        ParkingTicket.objects.filter(
            status="COMPLETED"
        ).count()
    )

    total_revenue = (
        Payment.objects.aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    context = {
        "total_slots": total_slots,
        "free_slots": free_slots,
        "occupied_slots": occupied_slots,
        "active_tickets": active_tickets,
        "completed_tickets": completed_tickets,
        "total_revenue": total_revenue,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )


def vehicle_entry(request):

    vehicle_types = (
        VehicleType.objects.all()
    )

    if request.method == "POST":

        vehicle_number = (
            request.POST.get(
                "vehicle_number",
                ""
            )
            .strip()
            .upper()
        )

        vehicle_type_id = (
            request.POST.get(
                "vehicle_type",
                ""
            )
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

                vehicle, created = (
                    ParkingService.register_vehicle(
                        vehicle_number,
                        vehicle_type_id
                    )
                )

                ticket = (
                    ParkingService.create_ticket(
                        vehicle
                    )
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
        "vehicle_types": vehicle_types
    }

    return render(
        request,
        "operations/vehicle_entry.html",
        context
    )


def ticket_detail(
    request,
    ticket_id
):

    ticket = (
        get_object_or_404(
            ParkingTicket,
            id=ticket_id
        )
    )

    context = {
        "ticket": ticket
    }

    return render(
        request,
        "operations/ticket_detail.html",
        context
    )

def vehicle_exit(request):

    ticket = None
    amount = None

    if request.method == "POST":

        action = request.POST.get(
            "action"
        )

        vehicle_number = request.POST.get(
            "vehicle_number",
            ""
        )

        ticket = (
            ParkingService.get_active_ticket(
                vehicle_number
            )
        )

        if not ticket:

            messages.error(
                request,
                "Active ticket not found."
            )

        else:

            amount = (
                PaymentService.calculate_amount(
                    ticket
                )
            )

            if action == "checkout":

                payment_method = (
                    request.POST.get(
                        "payment_method",
                        "CASH"
                    )
                )

                PaymentService.create_payment(
                    ticket,
                    payment_method
                )

                ParkingService.close_ticket(
                    ticket,
                    amount
                )

                SlotService.release_slot(
                    ticket.slot
                )

                messages.success(
                    request,
                    "Vehicle exited successfully."
                )

                return redirect(
                    "dashboard"
                )

    context = {
        "ticket": ticket,
        "amount": amount
    }

    return render(
        request,
        "operations/vehicle_exit.html",
        context
    )

def active_vehicles(request):

    tickets = (
        ParkingTicket.objects
        .filter(
            status="ACTIVE"
        )
        .select_related(
            "vehicle",
            "vehicle__vehicle_type",
            "slot"
        )
        .order_by(
            "-entry_time"
        )
    )

    context = {
        "tickets": tickets
    }

    return render(
        request,
        "operations/active_vehicles.html",
        context
    )

def vehicle_history(request):

    vehicles = (
        Vehicle.objects
        .select_related(
            "vehicle_type"
        )
        .order_by(
            "-visit_count"
        )
    )

    context = {
        "vehicles": vehicles
    }

    return render(
        request,
        "reports/vehicle_history.html",
        context
    )