"""Module for app tests."""


def test_healthcheck(client):
    """Function testing the app existence."""
    response = client.get("/_health")
    assert response.status_code == 204


def test_get_cities(client):
    """Function testing the GET city endpoint."""
    response = client.get("/city")
    assert response.status_code == 200


def test_insert_city(client):
    """Function testing the city insertion endpoint."""
    response = client.post("/city", json={
        "department_code": "989",
        "name": "Île de Clipperton",
        "lat": 10.30364715,
        "lon": -109.216321507291
    })
    assert response.status_code == 201
