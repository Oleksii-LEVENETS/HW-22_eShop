from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render

from orders.models import Order

from .forms import EditProfileForm, SignUpForm


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:  # noqa: R505
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect("shop:product_list")
        else:
            messages.success(request, "Error login in - Please Try Again!!!")
            return redirect("login")
    else:
        return render(request, "accounts/login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect("shop:product_list")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have been Registered!")
            return redirect("shop:product_list")

    else:
        form = SignUpForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def profile_user(request):
    orders = Order.objects.filter(email=request.user.email)
    return render(request, "accounts/profile.html", {"orders": orders})


def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Successfully Edited!")
            return redirect("shop:product_list")

    else:
        form = EditProfileForm(instance=request.user)

    context = {"form": form}
    return render(request, "accounts/edit_profile.html", context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Successfully Changed!")
            return redirect("shop:product_list")

    else:
        form = PasswordChangeForm(user=request.user)

    context = {"form": form}
    return render(request, "accounts/change_password.html", context)
