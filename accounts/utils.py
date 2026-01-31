from django.shortcuts import redirect


def redirect_after_login(user):
    if hasattr(user, "personal_profile"):
        if user.personal_profile.onboarding_completed:
            return redirect("personal-dashboard")
        return redirect("personal-onboarding")

    if hasattr(user, "business_profile"):
        if user.business_profile.onboarding_completed:
            return redirect("business-dashboard")
        return redirect("business-onboarding")

    return redirect("account-type")