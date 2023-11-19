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
    # competition = [
    #     {"name": "Test", "date": "2023-11-27 10:00:00", "numberOfPlaces": "25"}
    # ]
    # club = [{"name": "Test club", "email": "test@mail.com", "points": "10"}]
    competition = [
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"}
    ]
    club = [{"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}]

    club[0]["points"] = int(club[0]["points"])

    print("club : ", club)

    # Configuration initiale
    with app.app_context():
        app.competitions = competition
        app.clubs = club

    club_points_before = int(club[0]["points"])
    places_booked = 3

    print(type(club_points_before), club_points_before)
    print(type(places_booked), places_booked)
    print(type(club[0]["points"]), club[0]["points"])

    assert club[0]["points"] == club_points_before - places_booked
