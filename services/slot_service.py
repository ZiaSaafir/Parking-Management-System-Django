from parking.models import ParkingSlot


class SlotService:

    @staticmethod
    def get_free_slot():

        return (
            ParkingSlot.objects
            .filter(status="FREE")
            .order_by("slot_number")
            .first()
        )

    @staticmethod
    def occupy_slot(slot):

        slot.status = "OCCUPIED"

        slot.save()

        return slot

    @staticmethod
    def release_slot(slot):

        slot.status = "FREE"

        slot.save()

        return slot