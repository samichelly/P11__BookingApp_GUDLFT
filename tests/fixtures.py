import pytest
from flask import Flask
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        client.environ_base["HTTP_ACCEPT"] = "application/json"
        yield client


@pytest.fixture
def club_data():
    return {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "10"}


@pytest.fixture
def competition_data_one():
    return {
        "name": "Winter 2024",
        "date": "2024-01-22 13:30:00",
        "numberOfPlaces": "11",
    }


@pytest.fixture
def competition_data_two():
    return {
        "name": "Spring Festival",
        "date": "2024-03-27 10:00:00",
        "numberOfPlaces": "5",
    }
