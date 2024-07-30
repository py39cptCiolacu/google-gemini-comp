from __future__ import annotations

from flask import Blueprint, render_template, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import User

import folium


views = Blueprint("views", __name__)

points = [] # dc l am initializat pe asta aici? 

@views.route("/api/v1/user_profile", methods=["GET"])
@jwt_required()
def user_profile():
    current_user = get_jwt_identity()
    print(current_user)
    user = User.query.filter_by(email=current_user).first()
    if user:
        return jsonify(logged_in_as=current_user, email=user.email, username=user.username), 200
    return jsonify(message="User not found"), 404

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


