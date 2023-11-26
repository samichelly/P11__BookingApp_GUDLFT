import json
import pytest
from flask import Flask
from server import app
from .fixtures import client


# tests de la bonne déduction des points de club et place de compétition corrects
def test_deduct_points_deduct_places(client):
    competition_to_use = {
        "name": "Winter 2024",
        "numberOfPlaces": "42",
    }
    club_to_use = {
        "name": "The Strongest",
        "points": "10",
    }

    club_points_before_booking = int(club_to_use["points"])
    competition_places_before_booking = int(competition_to_use["numberOfPlaces"])
    places_booked = 3

    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_booked,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )

    response_data_dict = json.loads(response.data.decode("utf-8"))
    points_value = response_data_dict["club"]["points"]
    places_available_after = response_data_dict["competition"]["numberOfPlaces"]

    assert response.status_code == 200
    assert points_value == club_points_before_booking - places_booked
    assert places_available_after == competition_places_before_booking - places_booked
