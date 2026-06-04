from parking.models import Payment


class PaymentService:

    @staticmethod
    def generate_payment(ticket):

        amount = ticket.vehicle.vehicle_type.fixed_rate

        payment = Payment.objects.create(
            ticket=ticket,
            amount=amount,
            payment_method='CASH'
        )

        ticket.total_amount = amount
        ticket.save()

        return payment