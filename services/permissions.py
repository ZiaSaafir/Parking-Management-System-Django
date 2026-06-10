from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from parking.models import UserProfile


def role_required(*roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            profile, created = UserProfile.objects.get_or_create(
                user=request.user
            )

            if profile.role not in roles:

                messages.error(
                    request,
                    "Permission denied."
                )

                return redirect("login")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator