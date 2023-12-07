import pytest
import json
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
