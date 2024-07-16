from flask import Blueprint, render_template, request, jsonify
import folium

views = Blueprint("views", __name__)

points = []

@views.route('/')
def home() -> str:

    start_coords = (0, 0)
    folium_map= folium.Map(location=start_coords, zoom_start=2)

    return render_template("home.html", foium_map = folium_map._repr_html_())


@views.route("/get_coordinates", methods=["POST"])
def get_coordinates():

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

    return jsonify(response)





