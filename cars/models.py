import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


def db_uuid():
    return uuid.uuid4()


class Car(models.Model):
    class FuelType(models.TextChoices):
        PETROL = "P", _("PETROL")
        DIESEL = "D", _("DIESEL")
        HYBRID = "H", _("HYBRID")
        ELECTRIC = "E", _("ELECTRIC")

    engine_size = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    fuel_type = models.CharField(max_length=1, choices=FuelType, null=True)
    manufacturer = models.CharField(max_length=128, null=True)
    millage = models.PositiveIntegerField()
    model = models.CharField(max_length=128, null=True)
    price = models.PositiveIntegerField()
    uuid = models.UUIDField(primary_key=True, default=db_uuid)
    year_of_manufacture = models.PositiveSmallIntegerField()
