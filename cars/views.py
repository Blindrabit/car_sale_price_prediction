from django.db.models import Count, Avg
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


from cars.models import Car
from cars.serializer import CarSerializer


class CarsViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        "engine_size",
        "fuel_type",
        "manufacturer",
        "millage",
        "model",
        "price",
        "year_of_manufacture",
    )


class ManufacturerCountView(APIView):
    def get(self, request, *args, **kwargs):
        objects = (
            Car.objects.select_related()
            .values("manufacturer__uuid", "manufacturer__name")
            .annotate(count=Count("manufacturer"), average_price=Avg("price"))
            .order_by("-count")
        )
        return Response(objects)
