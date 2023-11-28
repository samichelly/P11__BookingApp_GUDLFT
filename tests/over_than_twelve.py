import json
import pytest
from flask import Flask, current_app
from server import app
from .fixtures import client


# tests des inputs en fonction de club et compétition
def test_select_less_than_12_places(client):
    competition_to_use = {
        "name": "Winter 2024",
    }

    club_to_use = {
        "name": "Simply Lift",
    }

    response = client.post(
        "/purchasePlaces",
        data={
            "places": 10,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )
    assert response.status_code == 200
    # ajouter le nombre de places restantes et le nombres de poonts restants


def test_select_more_than_12_places(client):
    competition_to_use = {
        "name": "Winter 2024",
    }

    club_to_use = {
        "name": "Iron Temple",
    }

    response = client.post(
        "/purchasePlaces",
        data={
            "places": 13,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )
    assert response.status_code == 400
    assert b'{"Error":"Cannot select more than 12 places"}' in response.data


def test_select_more_than_12_places_in_multiple_bookings(client):
    competition_to_use = {
        "name": "Winter 2024",
    }

    club_to_use = {
        "name": "Iron Temple",
    }
    response1 = client.post(
        "/purchasePlaces",
        data={
            "places": 10,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )
    assert response1.status_code == 200

    response2 = client.post(
        "/purchasePlaces",
        data={
            "places": 5,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )
    assert response2.status_code == 400


def test_select_more_than_club_points(client):
    competition_to_use = {
        "name": "Winter 2024",
    }

    club_to_use = {
        "name": "She Lifts",
    }

    response = client.post(
        "/purchasePlaces",
        data={
            "places": 11,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )

    print("\nresponse\n")
    print(response.data)
    print("\nresponse\n")
    assert response.status_code == 400
    assert b'{"Error":"Cannot select more places than the club has"}' in response.data


def test_select_more_than_competition_places(client):
    competition_to_use = {
        "name": "Spring Festival",
    }

    club_to_use = {
        "name": "Iron Temple",
    }

    response = client.post(
        "/purchasePlaces",
        data={
            "places": 10,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )
    assert response.status_code == 400
    assert (
        b'{"Error":"Cannot select more places than the competition has"}'
        or b'{"Error":"Cannot select more places than the club has"}' in response.data
    )


def test_select_negative_or_zero_places(client):
    competition_to_use = {
        "name": "Spring Festival",
    }

    club_to_use = {
        "name": "Iron Temple",
    }

    response = client.post(
        "/purchasePlaces",
        data={
            "places": -2,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )
    assert response.status_code == 400
    assert b'{"Error":"Invalid number of places"}' in response.data


def test_select_null_places(client):
    competition_to_use = {
        "name": "Spring Festival",
    }

    club_to_use = {
        "name": "Iron Temple",
    }

    response = client.post(
        "/purchasePlaces",
        data={
            "places": "",
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )
    assert response.status_code == 400
    assert b'{"Error":"Invalid number of places"}' in response.data
