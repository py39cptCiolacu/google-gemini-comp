from __future__ import annotations

from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User, LogedUser
from . import db
from .auth_helpers import is_valid_user, ValidateLogin

auth = Blueprint("auth", __name__)

@auth.route("/api/v1/login", methods=["POST"])
def login():
    data = request.json
    print("sall")
    if not data:
        print("0")
        return jsonify({"message": "No input data provided"}), 400
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        print("1")
        return jsonify({"message": "Email and password are required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        print("2")
        return jsonify({"message": "No such user"}), 401
    elif not check_password_hash(user.password, password):
        print("3")
        return jsonify({"message": "The password is incorrect"}), 401
    else:
        login_user(user, remember=True)
        
        print(f"Sunt aici {user.email}")
        print(current_user)
        session["user"] = "Daniel"

        worst_workaround_ever(current_user.email)

        return jsonify({"message": "Login successful!"}), 200


@auth.route("/api/v1/register", methods = ["GET", "POST"])
def register():
    
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    password_confirm = data.get("passwordConfirm")

    user = User.query.filter_by(email=email).first()

    is_valid = is_valid_user(user, username, email, password, password_confirm)

    if not is_valid.is_valid:
        return jsonify({"message" : f"{is_valid.flash_message}"}), 401
    else:
        new_user = User(email=email, username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return jsonify({"message": "Account created"}), 200

   

@auth.route("/api/v1/logout")
@login_required
def logout():
    logout_user()


def worst_workaround_ever(email: str) -> None:
    new_loged_used = LogedUser(email=email)
    db.session.add(new_loged_used)
    db.session.commit()