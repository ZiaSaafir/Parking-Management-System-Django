from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone

from parking.models import (
    ParkingTicket,
    Payment,
    ParkingSlot
)


def daily_report(request):

    today = timezone.now().date()

    entered_today = (
        ParkingTicket.objects.filter(
            entry_time__date=today
        ).count()
    )

    exited_today = (
        ParkingTicket.objects.filter(
            exit_time__date=today
        ).count()
    )

    revenue_today = (
        Payment.objects.filter(
            payment_time__date=today
        ).aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    active_tickets = (
        ParkingTicket.objects.filter(
            status="ACTIVE"
        ).count()
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

    context = {
        "entered_today": entered_today,
        "exited_today": exited_today,
        "revenue_today": revenue_today,
        "active_tickets": active_tickets,
        "free_slots": free_slots,
        "occupied_slots": occupied_slots,
    }

    return render(
        request,
        "reports/daily_report.html",
        context
    )