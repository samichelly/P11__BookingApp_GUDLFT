import json
import pytest
from flask import Flask
from server import app
from .fixtures import client


def test_deduct_points_deduct_places(client):
    competition_to_use = {
        "name": "Winter 2024",
    }
    club_to_use = {
        "name": "The Strongest",
    }
    places_booked = 3

    response1 = client.post(
        "/purchasePlaces",
        data={
            "places": 0,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )
    initial_state = json.loads(response1.data.decode("utf-8"))
    club_points_before_booking = initial_state["club"]["points"]
    competition_places_before_booking = initial_state["competition"]["numberOfPlaces"]

    response = client.post(
        "/purchasePlaces",
        data={
            "places": places_booked,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )
    updated_state = json.loads(response.data.decode("utf-8"))
    points_value = updated_state["club"]["points"]
    places_available_after = updated_state["competition"]["numberOfPlaces"]

    assert response.status_code == 200
    assert points_value == club_points_before_booking - places_booked
    assert places_available_after == competition_places_before_booking - places_booked
