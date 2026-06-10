import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

from services.permissions import role_required

from parking.models import (
    ParkingTicket,
    Payment,
    ParkingSlot
)


@login_required
@role_required("ADMIN", "MANAGER")
def daily_report(request):

    today = timezone.now().date()

    report_type = request.GET.get(
        "report_type",
        "today"
    )

    start_date = request.GET.get(
        "start_date"
    )

    end_date = request.GET.get(
        "end_date"
    )

    if report_type == "today":

        start_date = today
        end_date = today

    elif report_type == "month":

        start_date = today.replace(
            day=1
        )

        end_date = today

    elif report_type == "year":

        start_date = today.replace(
            month=1,
            day=1
        )

        end_date = today

    else:

        if not start_date:
            start_date = today

        if not end_date:
            end_date = today

    tickets = (
        ParkingTicket.objects
        .filter(
            entry_time__date__gte=start_date,
            entry_time__date__lte=end_date
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

    payments = (
        Payment.objects
        .filter(
            payment_time__date__gte=start_date,
            payment_time__date__lte=end_date
        )
        .select_related(
            "ticket",
            "ticket__vehicle",
            "ticket__vehicle__vehicle_type",
            "ticket__slot"
        )
    )

    entered_count = tickets.count()

    exited_count = tickets.filter(
        status="COMPLETED"
    ).count()

    revenue = (
        payments.aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    active_tickets = ParkingTicket.objects.filter(
        status="ACTIVE"
    ).count()

    free_slots = ParkingSlot.objects.filter(
        status="FREE"
    ).count()

    occupied_slots = ParkingSlot.objects.filter(
        status="OCCUPIED"
    ).count()

    if request.GET.get("export") == "csv":

        response = HttpResponse(
            content_type="text/csv"
        )

        response[
            "Content-Disposition"
        ] = "attachment; filename=parking_report.csv"

        writer = csv.writer(response)

        writer.writerow([
            "Ticket ID",
            "Vehicle Number",
            "Vehicle Type",
            "Slot",
            "Entry Time",
            "Exit Time",
            "Status",
            "Amount"
        ])

        for ticket in tickets:

            writer.writerow([
                ticket.id,
                ticket.vehicle.vehicle_number,
                ticket.vehicle.vehicle_type.name,
                ticket.slot.slot_number,
                ticket.entry_time,
                ticket.exit_time or "-",
                ticket.status,
                ticket.total_amount or 0
            ])

        return response

    context = {
        "report_type": report_type,
        "start_date": start_date,
        "end_date": end_date,
        "entered_count": entered_count,
        "exited_count": exited_count,
        "revenue": revenue,
        "active_tickets": active_tickets,
        "free_slots": free_slots,
        "occupied_slots": occupied_slots,
        "tickets": tickets,
    }

    return render(
        request,
        "reports/daily_report.html",
        context
    )