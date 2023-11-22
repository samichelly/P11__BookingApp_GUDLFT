# import json
# from flask import (
#     Flask,
#     render_template,
#     request,
#     redirect,
#     flash,
#     url_for,
#     jsonify,
# )
# from datetime import datetime


# def loadClubs():
#     with open("clubs.json") as c:
#         listOfClubs = json.load(c)["clubs"]
#         return listOfClubs


# def loadCompetitions():
#     with open("competitions.json") as comps:
#         listOfCompetitions = json.load(comps)["competitions"]
#         return listOfCompetitions


# app = Flask(__name__)
# app.secret_key = "something_special"

# app.competitions = loadCompetitions()
# app.clubs = loadClubs()


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/showSummary", methods=["POST"])
# def showSummary():
#     club = [club for club in app.clubs if club["email"] == request.form["email"]][0]
#     return render_template("welcome.html", club=club, competitions=app.competitions)


# @app.route("/book/<competition>/<club>")
# def book(competition, club):
#     (foundClub,) = [c for c in app.clubs if c["name"] == club]
#     (foundCompetition,) = [c for c in app.competitions if c["name"] == competition]

#     # competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
#     # current_date = datetime.now()

#     # if competition_date < current_date:
#     #     if (
#     #         request.accept_mimetypes.accept_json
#     #         and not request.accept_mimetypes.accept_html
#     #     ):
#     #         response_data = {"Error": "Past competition"}
#     #         return jsonify(response_data), 400
#     #     else:
#     #         flash("Past competition, choose another competition")
#     #         return render_template(
#     #             "welcome.html", club=club, competitions=app.competitions
#     #         )

#     if foundClub and foundCompetition:
#         return render_template(
#             "booking.html", club=foundClub, competition=foundCompetition
#         )
#     else:
#         flash("Something went wrong-please try again")
#         return render_template("welcome.html", club=club, competitions=app.competitions)


# # @app.route('/purchasePlaces',methods=['POST'])
# # def purchasePlaces():
# #     competition = [c for c in competitions if c['name'] == request.form['competition']][0]
# #     club = [c for c in clubs if c['name'] == request.form['club']][0]
# #     placesRequired = int(request.form['places'])
# #     competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
# #     flash('Great-booking complete!')
# #     return render_template('welcome.html', club=club, competitions=competitions)


# @app.route("/purchasePlaces", methods=["POST"])
# def purchasePlaces():
#     competition = [
#         c for c in app.competitions if c["name"] == request.form["competition"]
#     ][0]
#     club = [c for c in app.clubs if c["name"] == request.form["club"]][0]

#     competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
#     current_date = datetime.now()

#     if competition_date < current_date:
#         if (
#             request.accept_mimetypes.accept_json
#             and not request.accept_mimetypes.accept_html
#         ):
#             response_past_competition = {"Error": "Past competition"}
#             return jsonify(response_past_competition), 400
#         else:
#             flash("Past competition, choose another competition")
#             return render_template(
#                 "welcome.html", club=club, competitions=app.competitions
#             )

#     placesRequired = int(request.form["places"])

#     club["points"] = int(club["points"])

#     if placesRequired > 12:
#         if (
#             request.accept_mimetypes.accept_json
#             and not request.accept_mimetypes.accept_html
#         ):
#             response_overbooking = {"Error": "Cannot select more than 12 places"}
#             return jsonify(response_overbooking), 400
#         else:
#             flash("Cannot select more than 12 places")
#             return render_template(
#                 "welcome.html", club=club, competitions=app.competitions
#             )

#     if placesRequired > club["points"]:
#         if (
#             request.accept_mimetypes.accept_json
#             and not request.accept_mimetypes.accept_html
#         ):
#             response_overbooking = {
#                 "Error": "Cannot select more places than the club has"
#             }
#             return jsonify(response_overbooking), 400
#         else:
#             flash("Cannot select more places than the club has")
#             return render_template(
#                 "welcome.html", club=club, competitions=app.competitions
#             )

#     if placesRequired > int(competition["numberOfPlaces"]):
#         if (
#             request.accept_mimetypes.accept_json
#             and not request.accept_mimetypes.accept_html
#         ):
#             response_overbooking = {
#                 "Error": "Cannot select more places than the competition has"
#             }
#             return jsonify(response_overbooking), 400
#         else:
#             flash("Cannot select more places than the competition has")
#             return render_template(
#                 "welcome.html", club=club, competitions=app.competitions
#             )

#     competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired

#     club["points"] -= placesRequired

#     flash("Great-booking complete!")

#     if (
#         request.accept_mimetypes.accept_json
#         and not request.accept_mimetypes.accept_html
#     ):
#         response_data = {
#             "club": {
#                 "name": club["name"],
#                 "email": club["email"],
#                 "points": club["points"],
#             },
#             "competition": {
#                 "name": competition["name"],
#                 "date": competition["date"],
#                 "numberOfPlaces": competition["numberOfPlaces"],
#             },
#         }
#         return jsonify(response_data)
#     else:
#         return render_template("welcome.html", club=club, competitions=app.competitions)


# # TODO: Add route for points display


# @app.route("/logout")
# def logout():
#     return redirect(url_for("index"))


import json
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from datetime import datetime


app = Flask(__name__)
app.secret_key = "something_special"


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


app.competitions = load_competitions()
app.clubs = load_clubs()


class PastCompetitionError(Exception):
    pass


class OverbookingError(Exception):
    pass


def handle_error(error_message, status_code, club, competitions):
    if (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    ):
        response_data = {"Error": error_message}
        return jsonify(response_data), status_code
    else:
        flash(error_message)
        return render_template("welcome.html", club=club, competitions=competitions)


def check_overbooking(placesRequired, limit, error_message, club, competitions):
    if placesRequired > limit:
        raise OverbookingError(error_message)


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
        competition = next(
            c for c in app.competitions if c["name"] == request.form["competition"]
        )
        club = next(c for c in app.clubs if c["name"] == request.form["club"])

        competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
        current_date = datetime.now()

        if competition_date < current_date:
            raise PastCompetitionError("Past competition, choose another competition")

        placesRequired = int(request.form["places"])
        club["points"] = int(club["points"])

        check_overbooking(
            placesRequired,
            12,
            "Cannot select more than 12 places",
            club,
            app.competitions,
        )
        check_overbooking(
            placesRequired,
            club["points"],
            "Cannot select more places than the club has",
            club,
            app.competitions,
        )
        check_overbooking(
            placesRequired,
            int(competition["numberOfPlaces"]),
            "Cannot select more places than the competition has",
            club,
            app.competitions,
        )

        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        # competition["numberOfPlaces"] -= placesRequired
        club["points"] -= placesRequired

        flash("Great-booking complete!")

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
        return jsonify(response_data)

    except (StopIteration, PastCompetitionError, OverbookingError) as e:
        return handle_error(str(e), 400, club, app.competitions)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
