from __future__ import annotations

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from . import db
from .auth_helpers import is_valid_user, ValidateLogin

auth = Blueprint("auth", __name__)


@auth.route("/login", methods = ["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("The email address is not associated with any user account", category="error")

        if not check_password_hash(user.password, password):
            flash("Incorrect password", category="error")
        else:
            flash("Login succesfully", category="succes")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))

    return render_template("login.html", user=current_user)

@auth.route("/register", methods = ["GET", "POST"])
def register() -> str:
    
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password= request.form.get("password1")
        password_confirm= request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        is_valid = is_valid_user(user=user,
                                 username=username,
                                 email=email,
                                 password=password,
                                 password_confirm=password_confirm)

        if is_valid.is_valid == False:
            print("here")
            flash(is_valid.flash_message)
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created", category="succes")
            return redirect(url_for("views.home"))
        
    return render_template("register.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    login_user()