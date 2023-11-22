import json
import pytest
from flask import Flask
from server import app

import pdb


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.competition = {
        "name": "Winter 2024",
        "date": "2024-01-22 13:30:00",
        "numberOfPlaces": "13",
    }
    app.club = {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "10"}
    with app.test_client() as client:
        client.environ_base["HTTP_ACCEPT"] = "application/json"
        yield client


def test_deduct_points(client):
    # utilité de app_context
    # with app.app_context():
    #     app.competitions = competition
    #     app.clubs = club

    club_points_before_booking = int(app.club["points"])
    competition_places_before_booking = int(app.competition["numberOfPlaces"])
    places_booked = 3

    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_booked,
            "club": app.club["name"],
            "competition": app.competition["name"],
        },
    )

    response_data_dict = json.loads(response.data.decode("utf-8"))
    points_value = response_data_dict["club"]["points"]
    places_available_after = response_data_dict["competition"]["numberOfPlaces"]

    assert response.status_code == 200
    assert points_value == club_points_before_booking - places_booked
    assert places_available_after == competition_places_before_booking - places_booked
