from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import InvoiceForm, InvoiceItemCreateFormSet, InvoiceItemEditFormSet
from .models import Invoice, InvoiceStatus


@login_required
def invoice_list_view(request):
    invoices = Invoice.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    return render(
        request,
        "invoices/invoice_list.html",
        {"invoices": invoices},
    )

@login_required
def invoice_create_view(request):
    user = request.user

    if request.method == "POST":
        form = InvoiceForm(request.POST, user=user)
        formset = InvoiceItemCreateFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.owner = user
            invoice.save()

            formset.instance = invoice
            formset.save()

            return redirect("invoice-list")
    else:
        form = InvoiceForm(user=user)
        formset = InvoiceItemCreateFormSet()

    return render(
        request,
        "invoices/invoice_form.html",
        {"form": form, "formset": formset},
    )

@login_required
def invoice_detail_view(request, invoice_id):
    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        owner=request.user,
    )

    return render(
        request,
        "invoices/invoice_detail.html",
        {"invoice": invoice},
    )

@login_required
def invoice_mark_sent_view(request, invoice_id):
    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        owner=request.user,
    )

    if invoice.status == InvoiceStatus.DRAFT:
        invoice.status = InvoiceStatus.SENT
        invoice.save()

    return redirect("invoice-detail", invoice_id=invoice.id)

@login_required
def invoice_mark_paid_view(request, invoice_id):
    invoice = get_object_or_404(
        Invoice,
        id=invoice_id,
        owner=request.user,
    )

    if invoice.status == InvoiceStatus.SENT:
        invoice.status = InvoiceStatus.PAID
        invoice.save()

    return redirect("invoice-detail", invoice_id=invoice.id)

@login_required
def invoice_edit_view(request, pk):
    invoice = get_object_or_404(
        Invoice,
        pk=pk,
        owner=request.user,
        status=InvoiceStatus.DRAFT,
    )

    if request.method == "POST":
        form = InvoiceForm(
            request.POST,
            instance=invoice,
            user=request.user,          # ✅ OBAVEZNO
        )
        formset = InvoiceItemEditFormSet(request.POST, instance=invoice)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            return redirect("invoice-list")
    else:
        form = InvoiceForm(
            instance=invoice,
            user=request.user,          # ✅ OBAVEZNO
        )
        formset = InvoiceItemEditFormSet(instance=invoice)

    return render(
        request,
        "invoices/invoice_form.html",
        {
            "form": form,
            "formset": formset,
            "invoice": invoice,
            "is_edit": True,
        },
    )
@login_required
def invoice_delete_view(request, pk):
    invoice = get_object_or_404(
        Invoice,
        pk=pk,
        owner=request.user,
    )

    if invoice.status != InvoiceStatus.DRAFT:
        return redirect("invoice-list")

    if request.method == "POST":
        invoice.delete()
        return redirect("invoice-list")

    return render(
        request,
        "invoices/invoice_confirm_delete.html",
        {"invoice": invoice},
    )



