import pytest
from unittest.mock import patch, Mock

from django.urls import reverse

from cars.models import Car


def add_car(
    engine_size: str = "1.6",
    fuel_type: str = "P",
    manufacturer: str = "ford",
    millage: int = 12345,
    model: str = "Focus",
    price: int = 6789,
    year_of_manufacture: int = 1992,
):
    car = Car.objects.create(
        **{
            "engine_size": engine_size,
            "fuel_type": fuel_type,
            "manufacturer": manufacturer,
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
    response = client.post(
        url,
        data={
            "engine_size": "1.6",
            "fuel_type": "P",
            "manufacturer": "Ford",
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
        "manufacturer": "Ford",
        "millage": 12345,
        "model": "Focus",
        "price": 6789,
        "uuid": "9de2544d-b247-45d8-95da-2ccfcd6c1752",
        "year_of_manufacture": 1992,
    }


@patch("uuid.uuid4", Mock(return_value="9de2544d-b247-45d8-95da-2ccfcd6c1752"))
@pytest.mark.django_db
def test_car_list(client):
    add_car()
    url = reverse("cars-list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["results"] == [
        {
            "engine_size": "1.6",
            "fuel_type": "P",
            "manufacturer": "ford",
            "millage": 12345,
            "model": "Focus",
            "price": 6789,
            "uuid": "9de2544d-b247-45d8-95da-2ccfcd6c1752",
            "year_of_manufacture": 1992,
        }
    ]


@patch("uuid.uuid4", Mock(return_value="9de2544d-b247-45d8-95da-2ccfcd6c1752"))
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
            "manufacturer": "Toyota",
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
        "manufacturer": "Toyota",
        "millage": 67890,
        "model": "Focus",
        "price": 12345,
        "uuid": "9de2544d-b247-45d8-95da-2ccfcd6c1752",
        "year_of_manufacture": 2002,
    }


@patch("uuid.uuid4", Mock(return_value="9de2544d-b247-45d8-95da-2ccfcd6c1752"))
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
            "manufacturer": "Toyota",
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
        "manufacturer": "Toyota",
        "millage": 67890,
        "model": "Focus",
        "price": 12345,
        "uuid": "9de2544d-b247-45d8-95da-2ccfcd6c1752",
        "year_of_manufacture": 2002,
    }


@patch("uuid.uuid4", Mock(return_value="9de2544d-b247-45d8-95da-2ccfcd6c1752"))
@pytest.mark.django_db
def test_car_patch(client):
    car = add_car()
    url = reverse("cars-detail", kwargs={"pk": car.uuid})
    update_dict = {
        "engine_size": "2.0",
        "fuel_type": "H",
        "manufacturer": "Toyota",
        "millage": 67890,
        "model": "patch",
        "price": 12345,
        "uuid": "9de2544d-b247-45d8-95da-2ccfcd6c1752",
        "year_of_manufacture": 2002,
    }
    for k, v in update_dict.items():
        response = client.patch(
            url,
            content_type="application/json",
            data={k: v},
        )
        assert response.status_code == 200
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
    add_car()
    add_car(manufacturer="Toyota")
    url = reverse("manufacture-count")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == [
        {
            "manufacturer": "ford",
            "count": 2,
            "average_price": 6789.0,
        },
        {
            "manufacturer": "Toyota",
            "count": 1,
            "average_price": 6789.0,
        },
    ]
