import json
import pytest
from flask import Flask
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        client.environ_base["HTTP_ACCEPT"] = "application/json"
        yield client


def test_select_more_than_12_places(client):
    app.competition = {
        "name": "Winter 2024",
        "date": "2024-01-22 13:30:00",
        "numberOfPlaces": "11",
    }
    app.club = {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "10"}
    response = client.post(
        "/purchasePlaces",
        data={"places": 13, "club": "She Lifts", "competition": "Winter 2024"},
    )
    assert response.status_code == 400
    assert b'{"Error":"Cannot select more than 12 places"}' in response.data


def test_select_more_than_club_points(client):
    app.competition = {
        "name": "Winter 2024",
        "date": "2024-01-22 13:30:00",
        "numberOfPlaces": "11",
    }
    app.club = {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "10"}
    response = client.post(
        "/purchasePlaces",
        data={"places": 11, "club": "She Lifts", "competition": "Winter 2024"},
    )
    assert response.status_code == 400
    assert b'{"Error":"Cannot select more places than the club has"}' in response.data


def test_select_more_than_competition_places(client):
    app.competition = {
        "name": "Spring Festival",
        "date": "2024-03-27 10:00:00",
        "numberOfPlaces": "5",
    }
    app.club = {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "10"}
    response = client.post(
        "/purchasePlaces",
        data={"places": 10, "club": "She Lifts", "competition": "Spring Festival"},
    )
    assert response.status_code == 400
    assert (
        b'{"Error":"Cannot select more places than the competition has"}'
        in response.data
    )
