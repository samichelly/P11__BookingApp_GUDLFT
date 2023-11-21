import json
import pytest
from flask import Flask
from server import app
# from server.app import competitions, clubs
import pdb


# voir le decorateur
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        client.environ_base["HTTP_ACCEPT"] = "application/json"
        yield client


def test_deduct_points(client):
    # competition = [
    #     {"name": "Test", "date": "2023-11-17 10:00:00", "numberOfPlaces": "25"}
    # ]
    # club = [{"name": "Test club", "email": "test@mail.com", "points": "10"}]
    competition = {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13",
    }
    club = {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}

    # club["points"] = int(club["points"])

    # print("club : ", club)

    # utilité de app_context
    # with app.app_context():
    #     app.competitions = competition
    #     app.clubs = club

    pdb.set_trace()

    # club["points"] = int(club["points"])
    club_points_before_booking = int(club["points"])
    competition_places_before_booking = int(competition["numberOfPlaces"])
    places_booked = 3
    # expected_value = 9

    # print("app.competition[name] : ", app.competitions["name"])

    print("competition[name] : ", competition["name"])

    # print("app.competition[numberOfPlaces] : ", app.competitions["numberOfPlaces"])

    print("competition[numberOfPlaces] : ", competition["numberOfPlaces"])

    # competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - 4

    # print("test competition : ", competition["numberOfPlaces"])

    # print("app.competition[numberOfPlaces] : ", app.competitions["numberOfPlaces"])

    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_booked,
            "club": club["name"],
            "competition": competition["name"],
        },
    )

    response_data_dict = json.loads(response.data.decode("utf-8"))
    print(response_data_dict)
    points_value = response_data_dict["club"]["points"]
    places_available_after = response_data_dict["competition"]["numberOfPlaces"]

    print(type(places_booked), "places booked : ", places_booked)
    print(type(club["points"]), "nb points club avant réservation : ", club["points"])

    print("points_value = points restants : ", points_value)

    print("places_available_after = places dispo après resa : ", places_available_after)

    print("après test")

    # print("competition[name] : ", app.competitions["name"])

    # print("competition[numberOfPlaces] : ", app.competitions["numberOfPlaces"])

    assert response.status_code == 200
    # print(response)
    print(response.data)
    print(club["points"])
    assert points_value == club_points_before_booking - places_booked
    assert places_available_after == competition_places_before_booking - places_booked
    # assert expected_value == club_points_before_booking - places_booked


# def est-ce que l'evenement a baissé


# def jusqu'à 12

# def compet passé
