from rest_framework.serializers import ModelSerializer

from cars.models import Car


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = [
            "engine_size",
            "fuel_type",
            "manufacturer",
            "millage",
            "model",
            "price",
            "uuid",
            "year_of_manufacture",
        ]
