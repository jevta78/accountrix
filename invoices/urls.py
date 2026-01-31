from django.urls import path

from . import views

urlpatterns = [
    path("", views.invoice_list_view, name="invoice-list"),
    path("create/", views.invoice_create_view, name="invoice-create"),
    path("<int:invoice_id>/", views.invoice_detail_view, name="invoice-detail"),
path(
    "<int:invoice_id>/send/",views.invoice_mark_sent_view,name="invoice-mark-sent",
),
path(
    "<int:invoice_id>/paid/",views.invoice_mark_paid_view,name="invoice-mark-paid",
),
path("invoices/<int:pk>/edit/", views.invoice_edit_view, name="invoice-edit"),
path("invoices/<int:pk>/delete/", views.invoice_delete_view, name="invoice-delete"),
]