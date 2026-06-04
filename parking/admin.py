from django.contrib import admin
from .models import (
    VehicleType,
    Vehicle,
    ParkingSlot,
    ParkingTicket,
    Payment
)

admin.site.register(VehicleType)
admin.site.register(Vehicle)
admin.site.register(ParkingSlot)
admin.site.register(ParkingTicket)
admin.site.register(Payment)