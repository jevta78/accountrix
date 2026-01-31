from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClientForm
from .models import Client


@login_required
def client_list_view(request):
    clients = Client.objects.filter(owner=request.user).order_by("-created_at")
    return render(
        request,
        "clients/client_list.html",
        {"clients": clients},
    )


@login_required
def client_create_view(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = request.user
            client.save()
            return redirect("client-list")
    else:
        form = ClientForm()

    return render(
        request,
        "clients/client_form.html",
        {"form": form, "title": "Create client"},
    )


@login_required
def client_edit_view(request, client_id):
    client = get_object_or_404(
        Client,
        id=client_id,
        owner=request.user,
    )

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect("client-list")
    else:
        form = ClientForm(instance=client)

    return render(
        request,
        "clients/client_form.html",
        {"form": form, "title": "Edit client"},
    )


@login_required
def client_delete_view(request, client_id):
    client = get_object_or_404(
        Client,
        id=client_id,
        owner=request.user,
    )

    if request.method == "POST":
        client.delete()
        return redirect("client-list")

    return render(
        request,
        "clients/client_confirm_delete.html",
        {"client": client},
    )