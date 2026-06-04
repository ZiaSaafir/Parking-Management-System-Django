from django import forms

from .models import VehicleType


class VehicleEntryForm(forms.Form):

    vehicle_number = forms.CharField(
        max_length=20,
        label="Vehicle Number"
    )

    vehicle_type = forms.ModelChoiceField(
        queryset=VehicleType.objects.all(),
        label="Vehicle Type"
    )