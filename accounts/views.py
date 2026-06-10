from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth import (
    login,
    logout,
    authenticate
)

from django.contrib import messages

from .forms import (
    RegisterForm,
    LoginForm
)


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect(
                "dashboard"
            )

    else:

        form = RegisterForm()

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/register.html",
        context
    )


def login_view(request):

    if request.user.is_authenticated:

        return redirect(
            "dashboard"
        )

    if request.method == "POST":

        form = LoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get(
                "username"
            )

            password = form.cleaned_data.get(
                "password"
            )

            user = authenticate(
                username=username,
                password=password
            )

            if user:

                login(
                    request,
                    user
                )

                return redirect(
                    "dashboard"
                )

    else:

        form = LoginForm()

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/login.html",
        context
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect(
        "login"
    )