import json
import pytest
from flask import Flask
from server import app, book, purchasePlaces


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_deduct_points(client):
    # Données de test
    competition = [
        {"name": "Test", "date": "2023-11-27 10:00:00", "numberOfPlaces": "25"}
    ]
    club = [{"name": "Test club", "email": "testclub@email.com", "points": "10"}]

    # Configuration initiale
    with app.app_context():
        app.competitions = competition
        app.clubs = club

    # Réservation de places
    club_points_before = int(club[0]["points"])
    places_booked = 3

    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_booked,
            "club": club[0]["name"],
            "competition": competition[0]["name"],
        },
    )

    # Assertions
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()
    assert int(club[0]["points"]) == club_points_before - places_booked
