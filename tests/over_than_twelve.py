import json
import pytest
from flask import Flask
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.competition = {
        "name": "Winter 2024",
        "date": "2024-01-22 13:30:00",
        "numberOfPlaces": "13",
    }
    app.club = {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}

    with app.test_client() as client:
        client.environ_base["HTTP_ACCEPT"] = "application/json"
        yield client


def test_select_more_than_12_places(client):
    response = client.post(
        "/purchasePlaces",
        data={"places": 13, "club": "She Lifts", "competition": "Winter 2024"},
    )
    assert response.status_code == 400
    # print(response.data)
    assert b'{"Error":"Cannot select more than 12 places"}' in response.data
