from django.db import models


class VehicleType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    fixed_rate = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Vehicle(models.Model):

    vehicle_number = models.CharField(
        max_length=20,
        unique=True
    )

    vehicle_type = models.ForeignKey(
        VehicleType,
        on_delete=models.CASCADE
    )

    owner_name = models.CharField(
        max_length=100,
        blank=True
    )

    owner_phone = models.CharField(
        max_length=20,
        blank=True
    )

    visit_count = models.IntegerField(
        default=0
    )

    last_visit = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.vehicle_number

class ParkingSlot(models.Model):

    SLOT_STATUS = [
        ('FREE', 'Free'),
        ('OCCUPIED', 'Occupied'),
        ('MAINTENANCE', 'Maintenance'),
    ]

    slot_number = models.CharField(max_length=20, unique=True,db_index=True)

    status = models.CharField(
        max_length=20,
        choices=SLOT_STATUS,
        default='FREE'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slot_number
    

class ParkingTicket(models.Model):

    TICKET_STATUS = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    ]

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )

    slot = models.ForeignKey(
        ParkingSlot,
        on_delete=models.CASCADE
    )

    entry_time = models.DateTimeField(auto_now_add=True)

    exit_time = models.DateTimeField(
        null=True,
        blank=True
    )

    total_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=TICKET_STATUS,
        default='ACTIVE'
    )

    def __str__(self):
        return f"Ticket #{self.id}"
    
class Payment(models.Model):

    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
    ]

    ticket = models.OneToOneField(
        ParkingTicket,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    payment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id}"