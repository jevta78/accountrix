from django import forms
from django.forms import inlineformset_factory

from clients.models import Client

from .models import Invoice, InvoiceItem


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["client", "invoice_number"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["client"].queryset = Client.objects.filter(owner=user)


InvoiceItemCreateFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    fields=["description", "quantity", "unit_price"],
    extra=1,              # ✅ create → jedan prazan red
    can_delete=True,
)

InvoiceItemEditFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    fields=["description", "quantity", "unit_price"],
    extra=0,              # ✅ edit → NIJEDAN novi red
    can_delete=True,
)