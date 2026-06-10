from django import forms

from .models import ParkingSlot


class ParkingSlotForm(forms.ModelForm):

    class Meta:
        model = ParkingSlot

        fields = [
            "slot_number",
            "slot_type",
            "status"
        ]

        widgets = {
            "slot_number": forms.TextInput(
                attrs={
                    "placeholder": "Example: A-01"
                }
            ),

            "slot_type": forms.Select(),

            "status": forms.Select(),
        }