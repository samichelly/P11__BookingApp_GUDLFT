import json
import pytest
from flask import Flask
from server import app
from .fixtures import client, club_data, competition_data_one, competition_data_two


# tests des inputs en fonction de club et compétition
def test_select_more_than_12_places(client, competition_data_one, club_data):
    response = client.post(
        "/purchasePlaces",
        data={
            "places": 13,
            "club": club_data["name"],
            "competition": competition_data_one["name"],
        },
    )
    assert response.status_code == 400
    assert b'{"Error":"Cannot select more than 12 places"}' in response.data


def test_select_more_than_club_points(client, competition_data_one, club_data):
    response = client.post(
        "/purchasePlaces",
        data={
            "places": 11,
            "club": club_data["name"],
            "competition": competition_data_one["name"],
        },
    )
    assert response.status_code == 400
    assert b'{"Error":"Cannot select more places than the club has"}' in response.data


def test_select_more_than_competition_places(client, club_data, competition_data_two):
    response = client.post(
        "/purchasePlaces",
        data={
            "places": 10,
            "club": club_data["name"],
            "competition": competition_data_two["name"],
        },
    )
    assert response.status_code == 400
    assert (
        b'{"Error":"Cannot select more places than the competition has"}'
        or b'{"Error":"Cannot select more places than the club has"}' in response.data
    )


def test_select_negative_or_zero_places(client, club_data, competition_data_two):
    response = client.post(
        "/purchasePlaces",
        data={
            "places": -2,
            "club": club_data["name"],
            "competition": competition_data_two["name"],
        },
    )
    assert response.status_code == 400
    assert b'{"Error":"Invalid number of places"}' in response.data


def test_select_null_places(client, club_data, competition_data_two):
    response = client.post(
        "/purchasePlaces",
        data={
            "places": "",
            "club": club_data["name"],
            "competition": competition_data_two["name"],
        },
    )
    assert response.status_code == 400
    assert b'{"Error":"Invalid number of places"}' in response.data


# ajouter la réservation de plus de 12 en 2 fois
