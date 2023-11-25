import json
import pytest
from flask import Flask
from server import app
from .fixtures import client


def test_purchase_places_past_competition(client):
    past_competition = {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13",
    }

    response = client.post(
        "/purchasePlaces",
        data={
            "places": 3,
            "club": "She Lifts",
            "competition": past_competition["name"],
        },
    )

    assert b'{"Error":"Past competition, choose another competition"}' in response.data
    assert response.status_code == 400


def test_purchase_places_future_competition(client):
    future_competition = {
        "name": "Winter 2024",
        "date": "2024-01-22 13:30:00",
        "numberOfPlaces": "13",
    }

    response = client.post(
        "/purchasePlaces",
        data={
            "places": 3,
            "club": "She Lifts",
            "competition": future_competition["name"],
        },
    )

    assert b'{"Error":"Past competition"}' not in response.data
    assert response.status_code == 200
