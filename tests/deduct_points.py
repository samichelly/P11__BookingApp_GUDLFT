import json
import pytest
from flask import Flask
from server import app, loadCompetitions, loadClubs

import pdb


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.competition = {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13",
    }
    app.club = {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}
    with app.test_client() as client:
        client.environ_base["HTTP_ACCEPT"] = "application/json"
        yield client


# def setup():
#     app.competition = {
#         "name": "Fall Classic",
#         "date": "2020-10-22 13:30:00",
#         "numberOfPlaces": "13",
#     }
#     app.club = {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}


# def teardown():
#     # Réinitialiser les données après la fin des tests
#     app.competitions = loadCompetitions()
#     app.clubs = loadClubs()


def test_deduct_points(client):
    # competition = [
    #     {"name": "Test", "date": "2023-11-17 10:00:00", "numberOfPlaces": "25"}
    # ]
    # club = [{"name": "Test club", "email": "test@mail.com", "points": "10"}]
    # competition = {
    #     "name": "Fall Classic",
    #     "date": "2020-10-22 13:30:00",
    #     "numberOfPlaces": "13",
    # }
    # club = {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}

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
    print(response_data_dict)
    points_value = response_data_dict["club"]["points"]
    places_available_after = response_data_dict["competition"]["numberOfPlaces"]

    print(type(places_booked), "places booked : ", places_booked)
    print(
        type(app.club["points"]),
        "nb points club avant réservation : ",
        app.club["points"],
    )

    print("points_value = points restants : ", points_value)

    print("places_available_after = places dispo après resa : ", places_available_after)

    print("après test")

    assert response.status_code == 200
    # print(response)
    print(response.data)
    print(app.club["points"])
    assert points_value == club_points_before_booking - places_booked
    assert places_available_after == competition_places_before_booking - places_booked


# def jusqu'à 12
