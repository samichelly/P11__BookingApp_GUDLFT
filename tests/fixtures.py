import pytest
import json
from flask import Flask, current_app  # , create_app
from server import app


def load_test_clubs():
    with open("tests/test_clubs.json") as c:
        list_of_test_clubs = json.load(c)["clubs"]
        return list_of_test_clubs


def load_test_competitions():
    with open("tests/test_competitions.json") as comps:
        list_of_test_competitions = json.load(comps)["competitions"]
        return list_of_test_competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.competitions = load_test_competitions()
    app.clubs = load_test_clubs()
    with app.test_client() as client:
        yield client


# @pytest.fixture(scope="function")
# def club_data():
#     return {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "10"}


# @pytest.fixture(scope="function")
# def club_data_two():
#     return {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "34"}


# @pytest.fixture(scope="function")
# def club_data_for_multiple_booking():
#     return {"name": "Iron Strong", "email": "admin@ironstrong.com", "points": "34"}


# @pytest.fixture(scope="function")
# def competition_data_one():
#     return {
#         "name": "Winter 2024",
#         "date": "2024-01-22 13:30:00",
#         "numberOfPlaces": "42",
#     }


# @pytest.fixture(scope="function")
# def competition_data_two():
#     return {
#         "name": "Spring Festival",
#         "date": "2024-03-27 10:00:00",
#         "numberOfPlaces": "5",
#     }
