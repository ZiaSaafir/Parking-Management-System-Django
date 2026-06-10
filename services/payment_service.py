from decimal import Decimal

from django.utils import timezone

from parking.models import Payment


class PaymentService:

    @staticmethod
    def calculate_amount(ticket):
        """
        Calculate parking amount.
        Minimum charge is 1 hour.
        """

        exit_time = timezone.now()

        duration = exit_time - ticket.entry_time

        total_hours = duration.total_seconds() / 3600

        if total_hours < 1:
            total_hours = 1

        rate = ticket.vehicle.vehicle_type.fixed_rate

        amount = Decimal(str(total_hours)) * rate

        return round(amount, 2)

    @staticmethod
    def create_payment(ticket, payment_method):
        """
        Create payment record for completed parking ticket.
        """

        existing_payment = Payment.objects.filter(
            ticket=ticket
        ).first()

        if existing_payment:
            return existing_payment

        amount = PaymentService.calculate_amount(
            ticket
        )

        payment = Payment.objects.create(
            ticket=ticket,
            amount=amount,
            payment_method=payment_method
        )

        return payment