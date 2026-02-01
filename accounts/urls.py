from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("account-type/",
         views.account_type_view,
         name="account-type"),
    path("profile/edit/",
         views.personal_profile_edit_view,
         name="personal-profile-edit",),
    path("onboarding/personal/",
         views.personal_onboarding_view,
         name="personal-onboarding"),
    path("onboarding/business/",
         views.business_onboarding_view,
         name="business-onboarding"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("dashboard/personal/",
         views.personal_dashboard_view,
         name="personal-dashboard"),
    path("dashboard/business/",
         views.business_dashboard_view,
         name="business-dashboard")
]