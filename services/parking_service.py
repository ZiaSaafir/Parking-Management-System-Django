import re

from parking.models import (
    Vehicle,
    VehicleType
)


class ParkingService:

    @staticmethod
    def validate_vehicle_number(
        vehicle_number
    ):

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
        vehicle_type_id
    ):

        vehicle_number = (
            vehicle_number
            .strip()
            .upper()
            .replace("-", "")
            .replace(" ", "")
        )

        vehicle_type = VehicleType.objects.get(
            id=vehicle_type_id
        )

        vehicle, created = (
            Vehicle.objects.get_or_create(
                vehicle_number=vehicle_number,
                defaults={
                    "vehicle_type": vehicle_type
                }
            )
        )

        return vehicle, created