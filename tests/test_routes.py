"""Test routes of the HospitalTJ project."""
from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'name, identificator',
    (
        ('api:category-list', None),
        ('api:category-retrieve', 1),
        ('api:hospital-list', None),
        ('api:hospital-retrieve', 1),
        ('api:service-list', None),
        ('api:service-retrieve', 1),
    )
)
def test_endpoints_availability_for_anonymous_user(
        client, name, identificator) -> None:
    """Test endpoints availability for anonymous user at SAFE_METHODS."""
    url = reverse(name, args=(identificator,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_something(client):
    assert 5 == 2