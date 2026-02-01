from django.urls import path

from . import views

urlpatterns = [
    path("", views.client_list_view, name="client-list"),
    path("create/", views.client_create_view, name="client-create"),
    path("<int:client_id>/edit/",
         views.client_edit_view,
         name="client-edit"),
    path("<int:client_id>/delete/",
         views.client_delete_view,
         name="client-delete")
]