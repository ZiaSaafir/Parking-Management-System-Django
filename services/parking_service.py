import re
from decimal import Decimal

from django.utils import timezone
from django.db import transaction

from parking.models import (
    Vehicle,
    VehicleType,
    ParkingTicket
)

from services.slot_service import (
    SlotService
)


class ParkingException(Exception):
    """Base exception for parking service errors."""
    pass


class VehicleAlreadyParkedError(ParkingException):
    """Raised when trying to park an already parked vehicle."""
    pass


class NoSlotAvailableError(ParkingException):
    """Raised when no parking slots are available."""
    pass


class InvalidVehicleNumberError(ParkingException):
    """Raised when vehicle number format is invalid."""
    pass


class ParkingService:
    """
    Main service class for handling parking operations.
    Provides methods for vehicle registration, ticket creation,
    fee calculation, and ticket completion.
    """
    
    @staticmethod
    def normalize_vehicle_number(vehicle_number: str) -> str:
        """
        Normalize vehicle number by removing special characters and converting to uppercase.
        
        Args:
            vehicle_number: Raw vehicle number string
            
        Returns:
            Normalized vehicle number without spaces, dashes, in uppercase
        """
        return (
            vehicle_number
            .strip()          # Remove leading/trailing spaces
            .upper()          # Convert to uppercase
            .replace("-", "") # Remove hyphens
            .replace(" ", "") # Remove spaces
        )

    @staticmethod
    def validate_vehicle_number(vehicle_number: str) -> bool:
        """
        Validate vehicle number format using regex pattern.
        
        Args:
            vehicle_number: Vehicle number to validate
            
        Returns:
            True if valid, False otherwise
            
        Pattern Explanation:
            ^[A-Z0-9] - Must start with alphanumeric character
            {4,15}    - Length between 4 and 15 characters
            $         - End of string
        """
        # Normalize the vehicle number first
        normalized = ParkingService.normalize_vehicle_number(vehicle_number)
        
        # Regex pattern: Only uppercase letters and numbers, 4-15 characters long
        pattern = r"^[A-Z0-9]{4,15}$"
        
        return bool(re.match(pattern, normalized))

    @staticmethod
    def register_vehicle(vehicle_number: str, vehicle_type_id: int):
        """
        Register a new vehicle or retrieve existing one from database.
        
        Args:
            vehicle_number: Vehicle's registration number
            vehicle_type_id: ID of the vehicle type (car, bike, etc.)
            
        Returns:
            Tuple of (vehicle_object, created_flag)
            created_flag is True if new vehicle was created, False if existing
            
        Raises:
            VehicleType.DoesNotExist: If vehicle_type_id doesn't exist
        """
        # Clean and normalize the vehicle number
        normalized_number = ParkingService.normalize_vehicle_number(vehicle_number)
        
        # Validate the vehicle number format
        if not ParkingService.validate_vehicle_number(normalized_number):
            raise InvalidVehicleNumberError(
                f"Invalid vehicle number format: {vehicle_number}"
            )
        
        # Fetch the vehicle type from database
        # Will raise VehicleType.DoesNotExist if not found
        vehicle_type = VehicleType.objects.get(id=vehicle_type_id)
        
        # Get or create vehicle with the normalized number
        # get_or_create returns (object, created_flag)
        vehicle, created = Vehicle.objects.get_or_create(
            vehicle_number=normalized_number,
            defaults={
                "vehicle_type": vehicle_type
            }
        )
        vehicle.visit_count += 1

        vehicle.last_visit = (
        timezone.now()
        )

        vehicle.save()
        
        # If vehicle already existed but has different type, update it?
        # Current implementation doesn't update type for existing vehicles
        # This is intentional to maintain data consistency
        
        return vehicle, created

    @staticmethod
    @transaction.atomic
    def create_ticket(vehicle):
        """
        Create a new parking ticket for a vehicle.
        
        This method is atomic - if any step fails, all database changes are rolled back.
        
        Args:
            vehicle: Vehicle object to create ticket for
            
        Returns:
            Newly created ParkingTicket object
            
        Raises:
            VehicleAlreadyParkedError: If vehicle already has an active ticket
            NoSlotAvailableError: If no free parking slots available
        """
        # Check if vehicle already has an active parking ticket
        # An active ticket means the vehicle is currently parked
        active_ticket = ParkingTicket.objects.filter(
            vehicle=vehicle,
            status="ACTIVE"
        ).first()
        
        if active_ticket:
            raise VehicleAlreadyParkedError(
                f"Vehicle {vehicle.vehicle_number} is already parked."
            )
        
        # Find an available parking slot
        # SlotService handles the logic of finding free slots
        slot = SlotService.get_free_slot()
        
        if not slot:
            raise NoSlotAvailableError(
                "No parking slots available at the moment."
            )
        
        # Create the parking ticket
        # entry_time is auto-set by model's default=timezone.now
        ticket = ParkingTicket.objects.create(
            vehicle=vehicle,
            slot=slot
        )
        
        # Mark the slot as occupied
        # This prevents other vehicles from using the same slot
        SlotService.occupy_slot(slot)
        
        return ticket

    @staticmethod
    def get_active_ticket(vehicle_number: str):
        """
        Retrieve active ticket for a specific vehicle.
        
        Args:
            vehicle_number: Vehicle number to search for
            
        Returns:
            ParkingTicket object if found, None otherwise
        """
        # Normalize the vehicle number for consistent lookup
        normalized_number = ParkingService.normalize_vehicle_number(vehicle_number)
        
        # Query for active ticket using vehicle number
        # Uses double underscore to traverse the relationship
        return ParkingTicket.objects.filter(
            vehicle__vehicle_number=normalized_number,
            status="ACTIVE"
        ).first()

    @staticmethod
    def calculate_fee(ticket):
        """
        Calculate parking fee based on duration and vehicle type rate.
        
        Fee calculation logic:
        1. Calculate duration from entry_time to current time
        2. Round up to nearest hour (minimum 1 hour)
        3. Multiply hours by vehicle type's fixed rate
        
        Args:
            ticket: ParkingTicket object to calculate fee for
            
        Returns:
            Dictionary containing:
                - hours: Number of chargeable hours (minimum 1)
                - amount: Total amount to pay (Decimal)
        """
        # Get current timestamp
        now = timezone.now()
        
        # Calculate parking duration
        duration = now - ticket.entry_time
        
        # Convert duration to hours (total_seconds() / 3600)
        # Using integer division truncates down, so we cast to int
        # Example: 1.5 hours becomes 1 hour, 2.1 becomes 2 hours
        raw_hours = int(duration.total_seconds() / 3600)
        
        # Apply minimum charge of 1 hour
        # This ensures even a 15-minute stay is charged for 1 hour
        hours = max(1, raw_hours)
        
        # Get the hourly rate for this vehicle type
        # Access through vehicle relationship
        rate = ticket.vehicle.vehicle_type.fixed_rate
        
        # Calculate total amount using Decimal for precise currency math
        amount = Decimal(hours) * rate
        
        return {
            "hours": hours,
            "amount": amount
        }

    @staticmethod
    @transaction.atomic
    def complete_ticket(ticket):
        """
        Complete an active parking ticket and calculate final fee.
        
        This method is atomic - ensures fee calculation, ticket update,
        and slot release all succeed or fail together.
        
        Args:
            ticket: Active ParkingTicket object to complete
            
        Returns:
            Updated ParkingTicket object with exit_time, total_amount,
            and status set to COMPLETED
        """
        # Calculate final fee based on parking duration
        fee_data = ParkingService.calculate_fee(ticket)
        
        # Update ticket with exit information
        ticket.exit_time = timezone.now()          # Record when vehicle left
        ticket.total_amount = fee_data["amount"]   # Set calculated fee
        ticket.status = "COMPLETED"                # Mark as completed
        
        # Save all changes to database
        ticket.save()
        
        # Free up the parking slot for other vehicles
        SlotService.release_slot(ticket.slot)
        
        return ticket

    @staticmethod
    def close_ticket(ticket, amount):
        """
        Alternative method to close a ticket with manually specified amount.
        
        This method is useful for:
        - Manual fee adjustments
        - Special discounts or promotions
        - Handling edge cases where automatic calculation isn't appropriate
        
        Args:
            ticket: Active ParkingTicket object to close
            amount: Manual amount to charge (Decimal)
            
        Returns:
            Updated ParkingTicket object with exit_time, total_amount,
            and status set to COMPLETED
            
        Note:
            Unlike complete_ticket, this method does NOT automatically
            release the parking slot. The caller must ensure the slot
            is released separately if needed.
        """
        # Validate amount is positive
        if amount <= 0:
            raise ValueError(f"Amount must be positive, got {amount}")
        
        # Update ticket with manual amount
        ticket.exit_time = timezone.now()
        ticket.total_amount = amount
        ticket.status = "COMPLETED"
        ticket.save()
        
        # Note: Slot is NOT automatically released here
        # Caller should handle slot release if needed
        
        return ticket