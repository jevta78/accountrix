from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    BusinessProfileForm,
    PersonalProfileForm,
    UserRegisterForm,
)
from .models import BusinessProfile, PersonalProfile
from .utils import redirect_after_login

# =========================
# Home
# =========================

def home_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "accounts/home.html")


# =========================
# Register
# =========================

def register_view(request):
    if request.user.is_authenticated:
        return redirect_after_login(request.user)

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(
                request,
                user,
                backend="accounts.backends.EmailBackend",
            )

            return redirect("account-type")
    else:
        form = UserRegisterForm()

    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect_after_login(request.user)

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            email=email,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect_after_login(user)

        messages.error(request, "Invalid email or password")

    return render(request, "accounts/login.html")
# =========================
# Account Type
# =========================

@login_required
def account_type_view(request):
    user = request.user

    if hasattr(user, "personal_profile") or hasattr(user, "business_profile"):
        return redirect("dashboard")

    if request.method == "POST":
        account_type = request.POST.get("account_type")

        if account_type == "personal":
            PersonalProfile.objects.create(
                user=user,
                first_name="",
                last_name="",
            )
            return redirect("personal-onboarding")

        if account_type == "business":
            BusinessProfile.objects.create(
                owner=user,
                company_name="",
            )
            return redirect("business-onboarding")

    return render(request, "accounts/account_type.html")


# =========================
# Personal Onboarding
# =========================

@login_required
def personal_onboarding_view(request):
    profile = request.user.personal_profile

    if request.method == "POST":
        form = PersonalProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.onboarding_completed = True
            profile.save()
            return redirect("personal-dashboard")
    else:
        form = PersonalProfileForm(instance=profile)

    return render(
        request,
        "accounts/onboarding_personal.html",
        {"form": form},
    )


# =========================
# Business Onboarding
# =========================

@login_required
def business_onboarding_view(request):
    profile = request.user.business_profile

    if request.method == "POST":
        form = BusinessProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.onboarding_completed = True
            profile.save()
            return redirect("business-dashboard")
    else:
        form = BusinessProfileForm(instance=profile)

    return render(
        request,
        "accounts/onboarding_business.html",
        {"form": form},
    )


# =========================
# Dashboards
# =========================

@login_required
def dashboard_view(request):
    user = request.user

    if hasattr(user, "personal_profile"):
        return redirect("personal-dashboard")

    if hasattr(user, "business_profile"):
        return redirect("business-dashboard")

    return redirect("account-type")


@login_required
def personal_dashboard_view(request):
    return render(request, "accounts/dashboard_personal.html")


@login_required
def business_dashboard_view(request):
    return render(request, "accounts/dashboard_business.html")

@login_required
def personal_profile_edit_view(request):
    profile = request.user.personal_profile

    if request.method == "POST":
        form = PersonalProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("personal-dashboard")
    else:
        form = PersonalProfileForm(instance=profile)

    return render(
        request,
        "accounts/profile_edit.html",
        {"form": form},
    )

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")