import re

from django.utils import timezone

from parking.models import (
    Vehicle,
    VehicleType,
    ParkingTicket
)

from services.slot_service import SlotService
from services.payment_service import PaymentService


class ParkingService:

    @staticmethod
    def validate_vehicle_number(vehicle_number):
        """
        Validate vehicle number.
        """

        vehicle_number = (
            vehicle_number
            .strip()
            .upper()
            .replace("-", "")
            .replace(" ", "")
        )

        pattern = r"^[A-Z0-9]{4,15}$"

        return bool(
            re.match(
                pattern,
                vehicle_number
            )
        )

    @staticmethod
    def register_vehicle(
        vehicle_number,
        vehicle_type_id,
        owner_name="",
        owner_phone=""
    ):
        """
        Create vehicle if not exists.
        Update customer info if already exists.
        """

        vehicle_number = (
            vehicle_number
            .strip()
            .upper()
            .replace("-", "")
            .replace(" ", "")
        )

        try:
            vehicle_type = VehicleType.objects.get(
                id=vehicle_type_id
            )

        except VehicleType.DoesNotExist:
            raise Exception(
                "Invalid vehicle type."
            )

        vehicle, created = Vehicle.objects.get_or_create(
            vehicle_number=vehicle_number,
            defaults={
                "vehicle_type": vehicle_type,
                "owner_name": owner_name,
                "owner_phone": owner_phone,
            }
        )

        if not created:

            vehicle.vehicle_type = vehicle_type

            if owner_name:
                vehicle.owner_name = owner_name

            if owner_phone:
                vehicle.owner_phone = owner_phone

            vehicle.save()

        return vehicle, created

    @staticmethod
    def create_ticket(
        vehicle,
        slot_id=None
    ):
        """
        Create parking ticket.

        If operator selects slot, use selected free slot.
        Otherwise suggest compatible slot using vehicle type.
        """

        active_ticket = (
            ParkingTicket.objects
            .filter(
                vehicle=vehicle,
                status="ACTIVE"
            )
            .first()
        )

        if active_ticket:
            raise Exception(
                "Vehicle is already parked."
            )

        if slot_id:

            slot = SlotService.get_free_slot_by_id(
                slot_id
            )

            if not slot:
                raise Exception(
                    "Selected slot is not available."
                )

        else:

            slot = SlotService.get_suggested_slot(
                vehicle.vehicle_type.name
            )

            if not slot:
                raise Exception(
                    "No parking slot available."
                )

        ticket = ParkingTicket.objects.create(
            vehicle=vehicle,
            slot=slot
        )

        SlotService.occupy_slot(slot)

        vehicle.total_visits += 1
        vehicle.last_visit = timezone.now()
        vehicle.save()

        return ticket

    @staticmethod
    def get_active_ticket(vehicle_number):
        """
        Find active ticket by vehicle number.
        """

        vehicle_number = (
            vehicle_number
            .strip()
            .upper()
            .replace("-", "")
            .replace(" ", "")
        )

        return (
            ParkingTicket.objects
            .select_related(
                "vehicle",
                "slot"
            )
            .filter(
                vehicle__vehicle_number=vehicle_number,
                status="ACTIVE"
            )
            .first()
        )

    @staticmethod
    def close_ticket(ticket, amount):
        """
        Close parking ticket.
        """

        ticket.exit_time = timezone.now()
        ticket.total_amount = amount
        ticket.status = "COMPLETED"
        ticket.save()

        return ticket

    @staticmethod
    def process_exit(
        vehicle_number,
        payment_method
    ):
        """
        Complete vehicle exit workflow.
        """

        ticket = ParkingService.get_active_ticket(
            vehicle_number
        )

        if not ticket:
            raise Exception(
                "Active ticket not found."
            )

        amount = PaymentService.calculate_amount(
            ticket
        )

        payment = PaymentService.create_payment(
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

        return payment