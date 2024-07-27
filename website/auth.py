from __future__ import annotations

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db
from .auth_helpers import is_valid_user, ValidateLogin

auth = Blueprint("auth", __name__)


@auth.route("/api/v1/login", methods = ["GET", "POST"])
def login():

    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message" : "No such user"}), 401
    elif not check_password_hash(user.password, password):
        return jsonify({"message": "The passoword is incorect"}), 401
    else:
        return jsonify({"message": "Login succesful!"}), 200
    

@auth.route("/api/v1/register", methods = ["GET", "POST"])
def register() -> str:
    
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
    login_user()