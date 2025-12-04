import pytest
from unittest.mock import patch, Mock

from django.urls import reverse

from cars.models import Car, Manufacturer


def add_manufacturer(name: str = "ford") -> Manufacturer:
    manufacturer, _ = Manufacturer.objects.get_or_create(name=name)
    return manufacturer


def add_car(
    manufacturer_id: str | None = None,
    engine_size: str = "1.6",
    fuel_type: str = "P",
    millage: int = 12345,
    model: str = "Focus",
    price: int = 6789,
    year_of_manufacture: int = 1992,
):

    if manufacturer_id is None:
        manufacturer_id = str(add_manufacturer().uuid)
    car = Car.objects.create(
        **{
            "engine_size": engine_size,
            "fuel_type": fuel_type,
            "manufacturer_id": manufacturer_id,
            "millage": millage,
            "model": model,
            "price": price,
            "year_of_manufacture": year_of_manufacture,
        }
    )
    return car


@patch("uuid.uuid4", Mock(return_value="9de2544d-b247-45d8-95da-2ccfcd6c1752"))
@pytest.mark.django_db
def test_car_post(client):
    url = reverse("cars-list")
    manufacturer = add_manufacturer()
    response = client.post(
        url,
        data={
            "engine_size": "1.6",
            "fuel_type": "P",
            "manufacturer_id": manufacturer.uuid,
            "millage": 12345,
            "model": "Focus",
            "price": 6789,
            "year_of_manufacture": 1992,
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "engine_size": "1.6",
        "fuel_type": "P",
        "manufacturer": {"uuid": manufacturer.uuid, "name": manufacturer.name},
        "millage": 12345,
        "model": "Focus",
        "price": 6789,
        "uuid": "9de2544d-b247-45d8-95da-2ccfcd6c1752",
        "year_of_manufacture": 1992,
    }


@pytest.mark.django_db
def test_car_list(client):
    car = add_car()
    url = reverse("cars-list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["results"] == [
        {
            "engine_size": "1.6",
            "fuel_type": "P",
            "manufacturer": {
                "uuid": str(car.manufacturer.uuid),
                "name": car.manufacturer.name,
            },
            "millage": 12345,
            "model": "Focus",
            "price": 6789,
            "uuid": str(car.uuid),
            "year_of_manufacture": 1992,
        }
    ]


@pytest.mark.django_db
def test_car_patch(client):
    car = add_car()
    url = reverse("cars-detail", kwargs={"pk": car.uuid})
    response = client.put(
        url,
        content_type="application/json",
        data={
            "engine_size": "2.0",
            "fuel_type": "H",
            "millage": 67890,
            "model": "Focus",
            "price": 12345,
            "uuid": "9de2544d-b247-45d8-95da-2ccfcd6c1752",
            "year_of_manufacture": 2002,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "engine_size": "2.0",
        "fuel_type": "H",
        "manufacturer": {
            "uuid": str(car.manufacturer.uuid),
            "name": car.manufacturer.name,
        },
        "millage": 67890,
        "model": "Focus",
        "price": 12345,
        "uuid": str(car.uuid),
        "year_of_manufacture": 2002,
    }


@pytest.mark.django_db
def test_car_put(client):
    car = add_car()
    manufacturer = add_manufacturer("toyota")
    url = reverse("cars-detail", kwargs={"pk": car.uuid})
    response = client.put(
        url,
        content_type="application/json",
        data={
            "engine_size": "2.0",
            "fuel_type": "H",
            "manufacturer_id": str(manufacturer.uuid),
            "millage": 67890,
            "model": "Focus",
            "price": 12345,
            "year_of_manufacture": 2002,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "engine_size": "2.0",
        "fuel_type": "H",
        "manufacturer": {"uuid": str(manufacturer.uuid), "name": manufacturer.name},
        "millage": 67890,
        "model": "Focus",
        "price": 12345,
        "uuid": str(car.uuid),
        "year_of_manufacture": 2002,
    }


@pytest.mark.django_db
def test_car_patch(client):
    car = add_car()
    manufacturer = add_manufacturer("Toyota")
    url = reverse("cars-detail", kwargs={"pk": car.uuid})
    update_dict = {
        "engine_size": "2.0",
        "fuel_type": "H",
        "manufacturer_id": str(manufacturer.uuid),
        "millage": 67890,
        "model": "patch",
        "price": 12345,
        "year_of_manufacture": 2002,
    }
    for k, v in update_dict.items():
        response = client.patch(
            url,
            content_type="application/json",
            data={k: v},
        )
        assert response.status_code == 200
        if k == "manufacturer_id":
            assert response.json()["manufacturer"] == {
                "uuid": str(manufacturer.uuid),
                "name": manufacturer.name,
            }
        else:
            assert response.json()[k] == v


@pytest.mark.django_db
def test_car_delete(client):
    car = add_car()
    url = reverse("cars-detail", kwargs={"pk": car.uuid})
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_car_manufacture_count(client):
    add_car()
    car = add_car()
    manufacturer = add_manufacturer("Toyota")
    add_car(manufacturer_id=str(manufacturer.uuid))
    url = reverse("manufacture-count")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [
        {
            "manufacturer__uuid": str(car.manufacturer.uuid),
            "manufacturer__name": car.manufacturer.name,
            "count": 2,
            "average_price": 6789.0,
        },
        {
            "manufacturer__uuid": str(manufacturer.uuid),
            "manufacturer__name": manufacturer.name,
            "count": 1,
            "average_price": 6789.0,
        },
    ]
