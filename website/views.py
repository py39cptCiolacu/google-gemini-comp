from __future__ import annotations

from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user, login_user

import folium

from .models import User, LogedUser

views = Blueprint("views", __name__)

points = [] # dc l am initializat pe asta aici? 

# @views.route("/")
# def home() -> str:
    
#     return render_template("home.html")

@views.route("/test_loged_user", methods=["GET", "POST"])
# @login_required
def test_user_profile():
    if current_user.is_authenticated:
        print("e cnv logat")
        print(f"{current_user.email}")
    else:
        print("no user loged")

    return "<h1> salut </h1>"

@views.route("/login_bypass", methods=["GET", "POST"])
def login_bypass():

    user = User.query.filter_by(email="daniel@test.com").first()

    login_user(user, remember=True)

    return "<h1> all set </h1>"

@views.route("/api/v1/user_profile", methods=["GET"])
# @login_required
def user_profile():

    loged_user = LogedUser.query.order_by(LogedUser.id.desc()).first()
    user = User.query.filter_by(email = loged_user.email).first()


    return jsonify({"username": user.username  , "email": user.email}), 200

@views.route("/map")
def map() -> str:

    start_coords = (0, 0)
    folium_map= folium.Map(location=start_coords, zoom_start=2)

    return render_template("map.html", foium_map = folium_map._repr_html_())


@views.route("/get_coordinates", methods=["POST"])
def get_coordinates() -> dict:

    global points
    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")
    points.append((lat, lng))

    if len(points) > 4:
        points = points[-4:]

    response = {
        'lat': lat,
        'lng': lng,
        'points': points if len(points) == 4 else []
    }
    print(response)

    return jsonify(response)


