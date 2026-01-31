from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # Accounts app
    path("", include("accounts.urls")),
    path("clients/", include("clients.urls")),
    path("invoices/", include("invoices.urls")),
]