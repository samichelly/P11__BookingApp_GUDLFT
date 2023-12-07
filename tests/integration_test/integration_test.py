import json
from ..fixtures import client


def test_purchase_places_and_check_points(client):
    competition_to_use = {
        "name": "Winter 2024",
    }

    club_to_use = {
        "name": "Simply Lift",
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data={
            "places": 1,
            "club": club_to_use["name"],
            "competition": competition_to_use["name"],
        },
    )

    response_data = json.loads(response_purchase.data.decode("utf-8"))
    points_value = response_data["club"]["points"]
    assert response_purchase.status_code == 200

    response_index = client.get("/")
    response_index_data = json.loads(response_index.data.decode("utf-8"))

    club_to_use_data_index = None
    for club in response_index_data:
        if club["name"] == club_to_use["name"]:
            club_to_use_data_index = club
            break

    club_to_use_points_index = (
        club_to_use_data_index["points"] if club_to_use_data_index else None
    )
    assert response_index.status_code == 200
    assert points_value == club_to_use_points_index
