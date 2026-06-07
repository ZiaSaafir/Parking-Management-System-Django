from decimal import Decimal

from django.utils import timezone

from parking.models import Payment


class PaymentService:

    @staticmethod
    def calculate_amount(ticket):

        exit_time = timezone.now()

        duration = (
            exit_time -
            ticket.entry_time
        )

        total_hours = (
            duration.total_seconds() / 3600
        )

        if total_hours < 1:
            total_hours = 1

        rate = (
            ticket.vehicle
            .vehicle_type
            .fixed_rate
        )

        amount = (
            Decimal(total_hours) *
            rate
        )

        return round(amount, 2)

    @staticmethod
    def create_payment(
        ticket,
        payment_method
    ):

        amount = (
            PaymentService.calculate_amount(
                ticket
            )
        )

        payment = (
            Payment.objects.create(
                ticket=ticket,
                amount=amount,
                payment_method=payment_method
            )
        )

        return payment