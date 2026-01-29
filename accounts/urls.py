from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    dashboard_view,
    edit_profile_view,
    home_view,
    onboarding_view,
    register_view,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("onboarding/", onboarding_view, name="onboarding"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("profile/edit/", edit_profile_view, name="edit_profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", register_view, name="register"),
    path("login/", LoginView.as_view(template_name="public/login.html"), name="login"),
]