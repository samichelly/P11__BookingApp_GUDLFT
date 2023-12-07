import json
from ..fixtures import client


def test_valid_email(client):
    club_to_use = {
        "email": "admin@irontemple.com",
    }

    response = client.post(
        "/showSummary",
        data={
            "email": club_to_use["email"],
        },
    )

    json_response = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert club_to_use["email"] == json_response["email"]


def test_invalid_email(client):
    club_to_use = {
        "email": "unknow@email.com",
    }

    response = client.post(
        "/showSummary",
        data={
            "email": club_to_use["email"],
        },
    )

    assert response.status_code == 400
    assert b'{"Error":"Incorrect email"}' in response.data


def test_missing_email(client):
    club_to_use = {
        "email": "",
    }

    response = client.post(
        "/showSummary",
        data={
            "email": club_to_use["email"],
        },
    )

    assert response.status_code == 400
    assert b'{"Error":"Incorrect email"}' in response.data


def test_logout(client):
    response = client.get("/logout")

    assert response.status_code == 302
