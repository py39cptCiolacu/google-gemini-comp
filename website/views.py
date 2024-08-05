from __future__ import annotations

from flask import Blueprint, render_template, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import User, Land
from website import db

import folium


views = Blueprint("views", __name__)

points = [] # dc l am initializat pe asta aici? 

# @views.route("/api/v1/user_profile", methods=["GET"])
# @jwt_required()
# def user_profile():
#     current_user = get_jwt_identity()
#     print(current_user)
#     user = User.query.filter_by(email=current_user).first()
#     if user:
#         return jsonify(logged_in_as=current_user, email=user.email, username=user.username), 200
#     return jsonify(message="User not found"), 404

@views.route('/api/v1/user_profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    print(len(user.lands))
    print(user.id)

    user_profile = {
        "username": user.username,
        "email": user.email,
        "number_of_lands": len(user.lands),
        "lands" : [{'id': land.id, 'name':land.points, 'size': land.id} for land in user.lands]  
    }
    return jsonify(user_profile), 200


@views.route("/map")
@jwt_required()
def map() -> str:

    start_coords = (0, 0)
    folium_map= folium.Map(location=start_coords, zoom_start=2)

    return render_template("map.html", foium_map = folium_map._repr_html_())


@views.route("/get_coordinates", methods=["POST"])
@jwt_required()
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

@views.route("/api/v1/analysis", methods=["GET", "POST"])
@jwt_required()
def analysis() -> str:
    data = request.get_json()
    coords = data.get("points")
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    land = Land(user.id, coords)

    parameters = request.form.getlist("parameters")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    prompt = f"UserID: {user.id}; LandID: {land.id}; Parameters: {', '.join(parameters)}; Start Date: {start_date}; End Date: {end_date}"
    return prompt


@views.route("/add_land")
def add_land():

    new_land_1 = Land(1, [1, 2, 3, 4])
    new_land_2 = Land(1, [1, 2, 3, 5])

    db.session.add(new_land_1)
    db.session.add(new_land_2)

    db.session.commit()

    return "<h1> ADDED </h1>"