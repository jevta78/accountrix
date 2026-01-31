from django.conf import settings
from django.db import models
from django.db.models import F, Sum

from clients.models import Client


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PAID = "paid", "Paid"


class Invoice(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="invoices",
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    invoice_number = models.CharField(max_length=50)
    issue_date = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.DRAFT,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Invoice {self.invoice_number}"

    @property
    def total_amount(self):
        return (
            self.items.aggregate(
                total=Sum(F("quantity") * F("unit_price"))
            )["total"]
            or 0
        )


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items",
    )

    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.description

    @property
    def total(self):
        return self.quantity * self.unit_price