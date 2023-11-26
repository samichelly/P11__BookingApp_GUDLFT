import json
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from datetime import datetime
from collections import defaultdict


app = Flask(__name__)
app.secret_key = "something_special"

app.config["TESTING"] = True


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


def load_test_clubs():
    with open("tests/test_clubs.json") as c:
        list_of_test_clubs = json.load(c)["clubs"]
        return list_of_test_clubs


def load_test_competitions():
    with open("tests/test_competitions.json") as comps:
        list_of_test_competitions = json.load(comps)["competitions"]
        return list_of_test_competitions


if app.config.get("TESTING"):
    # Utilisez les données de test
    print("\nTRUE\n")
    app.config["competitions"] = load_test_competitions()
    app.config["clubs"] = load_test_clubs()
else:
    # Utilisez les données normales
    print("\nFALSE\n")
    app.config["competitions"] = load_competitions()
    app.config["clubs"] = load_clubs()


app.competitions = app.config["competitions"]
app.clubs = app.config["clubs"]

# def load_clubs():
#     with open("clubs.json") as c:
#         list_of_clubs = json.load(c)["clubs"]
#         return list_of_clubs


# def load_competitions():
#     with open("competitions.json") as comps:
#         list_of_competitions = json.load(comps)["competitions"]
#         return list_of_competitions


# app.competitions = load_competitions()
# app.clubs = load_clubs()

# competitions = load_competitions()
# clubs = load_clubs()

reserved_places = defaultdict(int)


class PastCompetitionError(Exception):
    pass


class OverbookingError(Exception):
    pass


def handle_error(error_message, status_code, club, competitions):
    # if (
    #     request.accept_mimetypes.accept_json
    #     and not request.accept_mimetypes.accept_html
    # ):
    if app.config["TESTING"] is True:
        response_data = {"Error": error_message}
        return jsonify(response_data), status_code
    else:
        flash(error_message)
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    club = next(
        (club for club in app.clubs if club["email"] == request.form["email"]), None
    )
    if club is None:
        flash("Club not found")
        return render_template("index.html")
    return render_template("welcome.html", club=club, competitions=app.competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = next((c for c in app.clubs if c["name"] == club), None)
    found_competition = next(
        (c for c in app.competitions if c["name"] == competition), None
    )

    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("index.html")


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    try:
        # print("competitions : ", app.competitions)
        competition = next(
            c for c in app.competitions if c["name"] == request.form["competition"]
        )
        # print("competition : ", competition)
        club = next(c for c in app.clubs if c["name"] == request.form["club"])
        # print("club : ", club)
        competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
        current_date = datetime.now()

        if competition_date < current_date:
            raise PastCompetitionError("Past competition, choose another competition")

        places_required_str = request.form["places"]
        if not places_required_str.isdigit() or int(places_required_str) <= 0:
            raise ValueError("Invalid number of places")

        placesRequired = int(request.form["places"])

        total_reserved_places = reserved_places[(club["name"], competition["name"])]
        # print("total_reserved_places : ", total_reserved_places)
        # print("placesRequired : ", placesRequired)
        if total_reserved_places + placesRequired > 12:
            raise OverbookingError(
                f"Cannot select more than 12 places"  # , you have already {total_reserved_places}
            )

        club["points"] = int(club["points"])

        if placesRequired > 12:
            raise OverbookingError("Cannot select more than 12 places")

        elif placesRequired > club["points"]:
            raise OverbookingError("Cannot select more places than the club has")

        elif placesRequired > int(competition["numberOfPlaces"]):
            raise OverbookingError("Cannot select more places than the competition has")

        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )

        club["points"] -= placesRequired

        reserved_places[(club["name"], competition["name"])] += placesRequired

        response_data = {
            "club": {
                "name": club["name"],
                "email": club["email"],
                "points": club["points"],
            },
            "competition": {
                "name": competition["name"],
                "date": competition["date"],
                "numberOfPlaces": competition["numberOfPlaces"],
            },
        }
        # if (
        #     request.accept_mimetypes.accept_json
        #     and not request.accept_mimetypes.accept_html
        # ):
        if app.config["TESTING"] is True:
            return jsonify(response_data)
        else:
            flash("Great-booking complete!")
            return render_template(
                "welcome.html", club=club, competitions=app.competitions
            )

    except (StopIteration, PastCompetitionError, OverbookingError, ValueError) as e:
        return handle_error(str(e), 400, club, app.competitions)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
