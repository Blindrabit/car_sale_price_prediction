from django.urls import path
from rest_framework.routers import DefaultRouter

from cars.views import CarsViewSet, ManufacturerCountView

urlpatterns = [
    path("manufacture-count/", ManufacturerCountView.as_view(), name="manufacture-count"),
]
router = DefaultRouter()
router.register(r"", CarsViewSet, basename="cars")
urlpatterns += router.urls
