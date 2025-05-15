from flask import Flask, render_template, request, jsonify
import googlemaps
import os
from utils.google_maps_api import (
    get_distance_and_duration,
    get_directions,
    get_lat_lng,
)

app = Flask(__name__)
gmaps = googlemaps.Client(key="AIzaSyDJE5HiSRrXoihhHGoGQ1J-SX0u_9BeL7I")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_traffic_prediction', methods=['POST'])
def get_traffic_prediction():
    try:
        data = request.get_json()
        source = data['source']
        destination = data['destination']
        vehicle_type = data['vehicle_type']
        vehicle_speed = float(data['vehicle_speed'])

        if not source or not destination:
            return jsonify({"error": "Source and destination must be provided."})

        # Get distance from Google API
        distance_duration_info = get_distance_and_duration(source, destination)
        if "error" in distance_duration_info:
            return jsonify({"error": distance_duration_info["error"]})

        # Convert distance string (e.g., "8.2 km") to float
        distance_km = float(distance_duration_info["distance"].replace(" km", "").replace(",", ""))

        # Calculate predicted time based on user speed
        if vehicle_speed <= 0:
            return jsonify({"error": "Speed must be greater than zero."})
        
        predicted_time_minutes = (distance_km / vehicle_speed) * 60
        hours = int(predicted_time_minutes // 60)
        minutes = int(predicted_time_minutes % 60)
        predicted_time_formatted = f"{hours} hours {minutes} mins"

        # Get directions for map
        directions_info = get_directions(source, destination)
        if "error" in directions_info:
            return jsonify({"error": directions_info["error"]})

        return jsonify({
            "source": source,
            "destination": destination,
            "distance": distance_duration_info["distance"],
            "duration": distance_duration_info["duration"],
            "predicted_time": predicted_time_formatted,
            "directions": directions_info
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/get_shortest_path', methods=['POST'])
def get_shortest_path():
    data = request.get_json()
    source = data.get('source')
    destination = data.get('destination')

    if not source or not destination:
        return jsonify({"error": "Source and destination are required."}), 400

    try:
        directions_result = gmaps.directions(
            origin=source,
            destination=destination,
            mode="driving",
            alternatives=False  # If you want shortest path only
        )

        if not directions_result:
            return jsonify({"error": "No route found."}), 404

        return jsonify({"shortest_path": directions_result[0]})  # Return only the first/shortest route

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=4000)
