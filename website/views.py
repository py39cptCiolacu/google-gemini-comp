from __future__ import annotations

from flask import Blueprint, render_template, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import User, Land
from website import db

import folium

views = Blueprint("views", __name__)

points = []  # dc l am initializat pe asta aici? 

# @views.route('/api/v1/user_profile', methods=['GET'])
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
        "lands": [{'id': land.id, 'name': land.name, 'size': land.get_area_surface()} for land in user.lands]  
    }
    return jsonify(user_profile), 200


@views.route('/api/v1/update_username', methods=['POST'])
@jwt_required()
def update_username():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    new_username = data.get('username')

    if not new_username:
        return jsonify({'error': 'Username cannot be empty'}), 400

    # Verifică dacă username-ul este deja folosit de un alt utilizator
    if User.query.filter_by(username=new_username).first():
        return jsonify({'error': 'Username already taken'}), 400

    # Actualizează username-ul utilizatorului curent
    user.username = new_username
    db.session.commit()

    return jsonify({'message': 'Username updated successfully', 'username': new_username}), 200


@views.route("/api/v1/add_land", methods=["POST"])
@jwt_required()
def add_land():

    current_user_jwt = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_jwt).first()

    data = request.json
    points = data.get("points", [])
    name = data.get("name")

    if len(points) != 4:
        return jsonify({'error' : 'You must provide exactly 4 points'}), 400
    
    print(points)
    print(name)
    new_land = Land(name=name, user_id=current_user.id,
                    x1=points[0][0],
                                 y1=points[0][1],
                                 x2=points[1][0],
                                 y2=points[1][1],
                                 x3=points[2][0],
                                 y3=points[2][1],
                                 x4=points[3][0],
                                 y4=points[3][1])

    surface = new_land.get_area_surface()
    print(surface)

    if surface > 3.00:
        return jsonify({'message': 'The surface must be smaller then 3'}), 400

    db.session.add(new_land)
    db.session.commit()
    return jsonify({'message': 'Land added succesfully'}), 200


@views.route("api/v1/get_coordinates", methods=["POST"])
# @jwt_required()
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
    # print(response)

    return jsonify(response)

@views.route('/api/v1/user_lands', methods=['GET'])
@jwt_required()
def get_user_lands():
    current_user_jwt = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_jwt).first()
    if current_user is None:
        return jsonify({"message": "User not found"}), 404
    
    lands = [{'id': land.id, 'name': land.name} for land in current_user.lands]
    return jsonify(lands), 200


# @views.route("/api/v1/analysis", methods=["GET", "POST"])
# @jwt_required()
# def analysis() -> str:
#     data = request.get_json()
#     coords = data.get("points")
#     current_user = get_jwt_identity()
#     user = User.query.filter_by(email=current_user).first()
#     land = Land(user.id, coords)

#     parameters = request.form.getlist("parameters")
#     start_date = request.form.get("start_date")
#     end_date = request.form.get("end_date")

#     dict_prompt = { "user": f"{user.id}",
#                    "parameters": [],
#                    "year": "",
#                    "month": [''],
#                    "day": [''],
#                    "area": land.get_limits()
#                    }

#     prompt = f"UserID: {user.id}; LandID: {land.id}; Parameters: {', '.join(parameters)}; Start Date: {start_date}; End Date: {end_date}"
#     return dict_prompt

@views.route('/api/v1/analysis', methods=['POST'])
@jwt_required()
def analysis():
    data = request.json
    params = data.get("parameters")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    land_id = data.get("land_id")
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    land = Land.query.filter_by(id=land_id, user_id=user.id).first()
    if not land:
        return jsonify({"message": "Land not found"}), 404

    dict_prompt = {
        "user": f"{user.id}",
        "land_id": f"{land.id}",
        "parameters": params,
        "start_date": start_date,
        "end_date": end_date,
        "area": land.get_limits()
    }

    # Process the analysis here and return the results
    return jsonify(dict_prompt), 200


# @views.route("/add_land")
# def add_land():

#     new_land_1 = Land(1, [1, 2, 3, 4])
#     new_land_2 = Land(1, [1, 2, 3, 5])

#     db.session.add(new_land_1)
#     db.session.add(new_land_2)

#     db.session.commit()

#     return "<h1> ADDED </h1>"

# @views.route("/test")
# def test():

#     # test_fetch()
#     # test_convertor()
#     process_json("test_username_test_land_2024_08_07_00_22_45.json", "results.json")

# #     return "<h1> ALL GOOD </h1"


# @views.route("/add_lands")
# def add_lands():

#     new_land_1 = Land("Land 1", 1, 12, 12, 44, 44, 55, 55, 66, 66)
#     new_land_2 = Land("Land 2", 1, 13, 13, 23, 12, 12, 23, 12, 34)

#     db.session.add(new_land_1)
#     db.session.add(new_land_2)

#     db.session.commit()

#     return "ALL GOOD"
