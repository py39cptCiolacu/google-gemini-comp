from __future__ import annotations

from flask import Blueprint, render_template, request, jsonify

auth = Blueprint("auth", __name__)


@auth.route("/login", methos = ["GET"])
def login():
    pass


@auth.route("/register", methos = ["GET"])
def register():
    pass


@auth.route("/logout")
def logout():
    pass