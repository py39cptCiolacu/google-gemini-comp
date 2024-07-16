from __future__ import annotations

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "a random string"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:////{DB_NAME}"
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

    return app

def create_database(app: Flask) -> None:
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Database Created")
