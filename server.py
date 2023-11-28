import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    jsonify,
    current_app,
)
from datetime import datetime
from collections import defaultdict
import os


CURRENT_DATE = datetime.now()

print(CURRENT_DATE)


app = Flask(__name__)
app.secret_key = "something_special"

# app.config["TESTING"] = True


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
    print("\nTRUE\n")
    app.config["competitions"] = load_test_competitions()
    app.config["clubs"] = load_test_clubs()
else:
    print("\nFALSE\n")
    app.config["competitions"] = load_competitions()
    app.config["clubs"] = load_clubs()


# def configure_app():
#     if "PYTEST_CURRENT_TEST" in os.environ:
#         app.config["TESTING"] = True
#         print("\nTRUE\n")
#         # Si le script est exécuté par pytest, utilisez les données de test
#         app.config["competitions"] = load_test_competitions()
#         app.config["clubs"] = load_test_clubs()
#     else:
#         # Sinon, utilisez les données normales
#         app.config["competitions"] = load_competitions()
#         app.config["clubs"] = load_clubs()

# configure_app()


app.competitions = app.config["competitions"]
app.clubs = app.config["clubs"]
reserved_places = defaultdict(int)


# upcoming_competitions = [
#     comp
#     for comp in app.competitions
#     if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > CURRENT_DATE
# ]
# past_competitions = [
#     comp
#     for comp in app.competitions
#     if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") <= CURRENT_DATE
# ]


def get_upcoming_competitions(competitions, current_date):
    return [
        comp
        for comp in competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > current_date
    ]


def get_past_competitions(competitions, current_date):
    return [
        comp
        for comp in competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") <= current_date
    ]


class PastCompetitionError(Exception):
    pass


class OverbookingError(Exception):
    pass


def handle_error(error_message, status_code, club, competitions):
    if app.config.get("TESTING"):
        response_data = {"Error": error_message}
        return jsonify(response_data), status_code
    else:
        flash(error_message)
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/")
def index():
    clubs_sorted = sorted(app.clubs, key=lambda x: x["name"])
    return render_template("index.html", clubs=clubs_sorted)


@app.route("/showSummary", methods=["POST"])
def show_summary():
    club = next(
        (club for club in app.clubs if club["email"] == request.form["email"]), None
    )
    if club is None:
        flash("Incorrect email. Please check your email and try again.", "error")
        return redirect(url_for("index"))

    upcoming_competitions = get_upcoming_competitions(app.competitions, CURRENT_DATE)
    past_competitions = get_past_competitions(app.competitions, CURRENT_DATE)

    return render_template(
        "welcome.html",
        club=club,
        upcoming_competitions=upcoming_competitions,
        past_competitions=past_competitions,
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    upcoming_competitions = get_upcoming_competitions(app.competitions, CURRENT_DATE)
    past_competitions = get_past_competitions(app.competitions, CURRENT_DATE)

    found_club = next((c for c in app.clubs if c["name"] == club), None)
    found_competition = next(
        (c for c in upcoming_competitions if c["name"] == competition), None
    )

    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html",
            club=found_club,
            upcoming_competitions=upcoming_competitions,
            past_competitions=past_competitions,
        )


@app.route("/purchasePlaces", methods=["POST", "GET"])
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
        CURRENT_DATE = datetime.now()

        if competition_date < CURRENT_DATE:
            raise PastCompetitionError("Past competition, choose another competition")

        if request.method == "POST":
            places_required_str = request.form["places"]
            if not places_required_str.isdigit() or int(places_required_str) <= 0:
                raise ValueError("Invalid number of places")

            placesRequired = int(request.form["places"])

            total_reserved_places = reserved_places[(club["name"], competition["name"])]

            if total_reserved_places + placesRequired > 12:
                raise OverbookingError("Cannot select more than 12 places")

            if placesRequired > 12:
                raise OverbookingError("Cannot select more than 12 places")

            elif placesRequired > club["points"]:
                raise OverbookingError("Cannot select more places than the club has")

            elif placesRequired > int(competition["numberOfPlaces"]):
                raise OverbookingError(
                    "Cannot select more places than the competition has"
                )

            competition["numberOfPlaces"] = (
                competition["numberOfPlaces"] - placesRequired
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

        print("response")
        print(response_data)
        print("response")

        # upcoming_competitions = get_upcoming_competitions(
        #     app.competitions, CURRENT_DATE
        # )
        # past_competitions = get_past_competitions(app.competitions, CURRENT_DATE)

        # if app.config["TESTING"] is True:
        #     return jsonify(response_data)
        # else:
        #     flash(f"Great - {placesRequired} place(s) booked !")
        #     return render_template(
        #         "welcome.html",
        #         club=club,
        #         upcoming_competitions=upcoming_competitions,
        #         past_competitions=past_competitions,
        #     )

    except (PastCompetitionError, OverbookingError, ValueError) as e:
        return handle_error(str(e), 400, club, app.competitions)

    else:
        if app.config["TESTING"] is True:
            return jsonify(response_data)
        else:
            flash(f"Great - {placesRequired} place(s) booked !")

    finally:
        upcoming_competitions = get_upcoming_competitions(
            app.competitions, CURRENT_DATE
        )
        past_competitions = get_past_competitions(app.competitions, CURRENT_DATE)

        if app.config["TESTING"] is not True:
            return render_template(
                "welcome.html",
                club=club,
                upcoming_competitions=upcoming_competitions,
                past_competitions=past_competitions,
            )


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
