from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from cars.models import Car, Manufacturer


class ManufacturerSerializer(ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = "__all__"


class CarSerializer(ModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)
    manufacturer_id = PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(), source="manufacturer", write_only=True
    )

    class Meta:
        model = Car
        fields = [
            "engine_size",
            "fuel_type",
            "manufacturer",
            "manufacturer_id",
            "millage",
            "model",
            "price",
            "uuid",
            "year_of_manufacture",
        ]
