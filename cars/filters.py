from django_filters import rest_framework as filters

from cars.models import Car


class CarFilter(filters.FilterSet):
    class Meta:
        model = Car
        fields = {
            "engine_size": ["lt", "gt"],
            "fuel_type": ["iexact"],
            "manufacturer": ["iexact"],
            "millage": ["lt", "gt"],
            "model": ["iexact"],
            "price": ["lt", "gt"],
            "year_of_manufacture": ["lt", "gt"],
        }
