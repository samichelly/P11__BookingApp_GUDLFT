import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    jsonify,
)
from datetime import datetime
from collections import defaultdict

CURRENT_DATE = datetime.now()

app = Flask(__name__)
app.secret_key = "something_special"

CLUBS_FILE = "clubs.json"
COMPETITIONS_FILE = "competitions.json"


def load_data(file_path):
    with open(file_path) as f:
        return json.load(f)


app.competitions = load_data(COMPETITIONS_FILE)["competitions"]
app.clubs = load_data(CLUBS_FILE)["clubs"]
reserved_places = defaultdict(int)


def get_upcoming_and_past_competitions(competitions, current_date):
    upcoming = []
    past = []

    for comp in competitions:
        comp_date = datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S")

        if comp_date > current_date:
            upcoming.append(comp)
        else:
            past.append(comp)

    return upcoming, past


class PastCompetitionError(Exception):
    pass


class OverbookingError(Exception):
    pass


def handle_error(error_message, status_code, club=None, competitions=None):
    if app.config.get("TESTING"):
        return jsonify({"Error": error_message}), status_code
    else:
        flash(error_message)
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/")
def index():
    clubs_sorted = sorted(app.clubs, key=lambda x: x["name"])
    return render_template("index.html", clubs=clubs_sorted)


@app.route("/showSummary", methods=["POST"])
def show_summary():
    email = request.form.get("email")
    club = next((c for c in app.clubs if c["email"] == email), None)

    if club is None:
        if app.config["TESTING"]:
            return jsonify({"Error": "Incorrect email"}), 400
        else:
            flash("Incorrect email. Please check your email and try again.", "error")
            return redirect(url_for("index"))

    upcoming_competitions, past_competitions = get_upcoming_and_past_competitions(
        app.competitions, CURRENT_DATE
    )

    if app.config["TESTING"]:
        return jsonify(club)

    return render_template(
        "welcome.html",
        club=club,
        upcoming_competitions=upcoming_competitions,
        past_competitions=past_competitions,
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    upcoming_competitions, past_competitions = get_upcoming_and_past_competitions(
        app.competitions, CURRENT_DATE
    )

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


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    try:
        (competition,) = (
            c for c in app.competitions if c["name"] == request.form["competition"]
        )
        (club,) = (c for c in app.clubs if c["name"] == request.form["club"])
    except ValueError:
        raise ValueError("No club or competition found")

    competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    places_required_str = request.form["places"]

    try:
        if competition_date < CURRENT_DATE:
            raise PastCompetitionError("Past competition, choose another competition")

        if not places_required_str.isdigit() or int(places_required_str) < 0:
            raise ValueError("Invalid number of places")

        placesRequired = int(places_required_str)

        total_reserved_places = reserved_places[(club["name"], competition["name"])]

        if total_reserved_places + placesRequired > 12:
            raise OverbookingError("Cannot select more than 12 places")

        elif placesRequired > club["points"]:
            raise OverbookingError("Cannot select more places than the club has")

        elif placesRequired > int(competition["numberOfPlaces"]):
            raise OverbookingError("Cannot select more places than the competition has")

        competition["numberOfPlaces"] -= placesRequired
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

    except (PastCompetitionError, OverbookingError, ValueError) as e:
        return handle_error(str(e), 400, club, app.competitions)

    else:
        if app.config["TESTING"]:
            return jsonify(response_data)
        else:
            flash(f"Great - {placesRequired} place(s) booked !")

    finally:
        upcoming_competitions, past_competitions = get_upcoming_and_past_competitions(
            app.competitions, CURRENT_DATE
        )

        if not app.config["TESTING"]:
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
