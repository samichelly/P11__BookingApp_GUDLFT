import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    jsonify,
    abort,
)
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

app.competitions = loadCompetitions()
app.clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = [club for club in app.clubs if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=app.competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    (foundClub,) = [c for c in app.clubs if c["name"] == club]
    (foundCompetition,) = [c for c in app.competitions if c["name"] == competition]

    # competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    # current_date = datetime.now()

    # if competition_date < current_date:
    #     if (
    #         request.accept_mimetypes.accept_json
    #         and not request.accept_mimetypes.accept_html
    #     ):
    #         response_data = {"Error": "Past competition"}
    #         return jsonify(response_data), 400
    #     else:
    #         flash("Past competition, choose another competition")
    #         return render_template(
    #             "welcome.html", club=club, competitions=app.competitions
    #         )

    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=app.competitions)


# @app.route('/purchasePlaces',methods=['POST'])
# def purchasePlaces():
#     competition = [c for c in competitions if c['name'] == request.form['competition']][0]
#     club = [c for c in clubs if c['name'] == request.form['club']][0]
#     placesRequired = int(request.form['places'])
#     competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
#     flash('Great-booking complete!')
#     return render_template('welcome.html', club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [
        c for c in app.competitions if c["name"] == request.form["competition"]
    ][0]
    club = [c for c in app.clubs if c["name"] == request.form["club"]][0]

    competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    current_date = datetime.now()

    if competition_date < current_date:
        if (
            request.accept_mimetypes.accept_json
            and not request.accept_mimetypes.accept_html
        ):
            response_past_competition = {"Error": "Past competition"}
            return jsonify(response_past_competition), 400
        else:
            flash("Past competition, choose another competition")
            return render_template(
                "welcome.html", club=club, competitions=app.competitions
            )

    placesRequired = int(request.form["places"])

    club["points"] = int(club["points"])

    if placesRequired > 12:
        response_overbooking = {"Error": "Cannot select more than 12 places"}
        return jsonify(response_overbooking), 400

    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired

    club["points"] -= placesRequired

    flash("Great-booking complete!")

    if (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    ):
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
    else:
        return render_template("welcome.html", club=club, competitions=app.competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
