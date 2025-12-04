import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


def db_uuid():
    return uuid.uuid4()


class Manufacturer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=db_uuid, editable=False)
    name = models.CharField(max_length=128, null=True)


class Car(models.Model):
    class FuelType(models.TextChoices):
        PETROL = "P", _("PETROL")
        DIESEL = "D", _("DIESEL")
        HYBRID = "H", _("HYBRID")
        ELECTRIC = "E", _("ELECTRIC")

    uuid = models.UUIDField(primary_key=True, default=db_uuid, editable=False)

    engine_size = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    fuel_type = models.CharField(max_length=1, choices=FuelType, null=True)
    millage = models.PositiveIntegerField()
    model = models.CharField(max_length=128, null=True)
    price = models.PositiveIntegerField()
    year_of_manufacture = models.PositiveSmallIntegerField()
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, editable=False
    )
