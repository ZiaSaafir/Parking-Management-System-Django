from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from django.contrib.auth.decorators import (
    login_required
)

from services.permissions import (
    role_required
)

from .models import (
    ParkingSlot
)

from .forms import (
    ParkingSlotForm
)


@login_required
@role_required("ADMIN")
def parking_slot_list(request):

    slots = (
        ParkingSlot.objects
        .all()
        .order_by(
            "slot_number"
        )
    )

    context = {
        "slots": slots
    }

    return render(
        request,
        "slots/slot_list.html",
        context
    )


@login_required
@role_required("ADMIN")
def parking_slot_create(request):

    form = ParkingSlotForm()

    if request.method == "POST":

        form = ParkingSlotForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Parking slot created successfully."
            )

            return redirect(
                "parking_slot_list"
            )

    context = {
        "form": form,
        "title": "Create Parking Slot",
        "button_text": "Save Slot"
    }

    return render(
        request,
        "slots/slot_form.html",
        context
    )


@login_required
@role_required("ADMIN")
def parking_slot_update(
    request,
    slot_id
):

    slot = get_object_or_404(
        ParkingSlot,
        id=slot_id
    )

    form = ParkingSlotForm(
        instance=slot
    )

    if request.method == "POST":

        form = ParkingSlotForm(
            request.POST,
            instance=slot
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Parking slot updated successfully."
            )

            return redirect(
                "parking_slot_list"
            )

    context = {
        "form": form,
        "title": "Update Parking Slot",
        "button_text": "Update Slot"
    }

    return render(
        request,
        "slots/slot_form.html",
        context
    )


@login_required
@role_required("ADMIN")
def parking_slot_delete(
    request,
    slot_id
):

    slot = get_object_or_404(
        ParkingSlot,
        id=slot_id
    )

    if slot.status == "OCCUPIED":

        messages.error(
            request,
            "Occupied slot cannot be deleted."
        )

        return redirect(
            "parking_slot_list"
        )

    if request.method == "POST":

        slot.delete()

        messages.success(
            request,
            "Parking slot deleted successfully."
        )

        return redirect(
            "parking_slot_list"
        )

    context = {
        "slot": slot
    }

    return render(
        request,
        "slots/slot_confirm_delete.html",
        context
    )