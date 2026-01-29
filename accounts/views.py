from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BusinessProfileForm, UserProfileForm, UserRegisterForm


@login_required
def onboarding_view(request):
    profile = request.user.profile

    if profile.onboarding_completed:
        return redirect("dashboard")

    if request.method == "POST":
        profile.onboarding_completed = True
        profile.save()
        return redirect("dashboard")

    return render(request, "accounts/onboarding.html")

@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")

def home_view(request):
    if not request.user.is_authenticated:
        return render(request, "public/home.html")

    profile = request.user.profile

    if not profile.onboarding_completed:
        return redirect("onboarding")

    return redirect("dashboard")


@login_required
def edit_profile_view(request):
    user_profile = request.user.profile
    business_profile = request.user.business

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=user_profile)
        business_form = BusinessProfileForm(request.POST, instance=business_profile)

        if user_form.is_valid() and business_form.is_valid():
            user_form.save()
            business_form.save()
            return redirect("dashboard")
    else:
        user_form = UserProfileForm(instance=user_profile)
        business_form = BusinessProfileForm(instance=business_profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "user_form": user_form,
            "business_form": business_form,
        },
    )
    
def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserRegisterForm()

    return render(request, "public/register.html", {"form": form})