from parking.models import ParkingSlot


class SlotService:

    @staticmethod
    def get_free_slots():
        """
        Return all free slots.
        """

        return (
            ParkingSlot.objects
            .filter(
                status="FREE"
            )
            .order_by(
                "slot_number"
            )
        )

    @staticmethod
    def get_free_slot():
        """
        Return first free slot.

        This keeps compatibility with existing views that call:
        SlotService.get_free_slot()
        """

        return (
            ParkingSlot.objects
            .filter(
                status="FREE"
            )
            .order_by(
                "slot_number"
            )
            .first()
        )

    @staticmethod
    def get_compatible_free_slots(
        vehicle_type_name
    ):
        """
        Return free slots compatible with vehicle type.

        Example:
        CAR can use CAR or ANY.
        BUS can use BUS or ANY.
        """

        if not vehicle_type_name:

            return SlotService.get_free_slots()

        vehicle_type_name = (
            vehicle_type_name
            .strip()
            .upper()
        )

        return (
            ParkingSlot.objects
            .filter(
                status="FREE",
                slot_type__in=[
                    vehicle_type_name,
                    "ANY"
                ]
            )
            .order_by(
                "slot_type",
                "slot_number"
            )
        )

    @staticmethod
    def get_suggested_slot(
        vehicle_type_name=None
    ):
        """
        Suggest best free slot.
        """

        if vehicle_type_name:

            compatible_slot = (
                SlotService
                .get_compatible_free_slots(
                    vehicle_type_name
                )
                .first()
            )

            if compatible_slot:

                return compatible_slot

        return SlotService.get_free_slot()

    @staticmethod
    def get_free_slot_by_id(
        slot_id
    ):
        """
        Return selected free slot by ID.
        """

        return (
            ParkingSlot.objects
            .filter(
                id=slot_id,
                status="FREE"
            )
            .first()
        )

    @staticmethod
    def occupy_slot(
        slot
    ):
        """
        Mark slot as occupied.
        """

        slot.status = "OCCUPIED"
        slot.save()

        return slot

    @staticmethod
    def release_slot(
        slot
    ):
        """
        Mark slot as free.
        """

        slot.status = "FREE"
        slot.save()

        return slot