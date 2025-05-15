import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key="AIzaSyCF-w2YjvvbBdombqO5Ap-Ek7cvnBYAlIA")

def get_distance_and_duration(source, destination):
    try:
        # Geocoding an address
        directions_result = gmaps.directions(source, destination, mode="driving", departure_time=datetime.now())
        print(directions_result)
        
        if not directions_result:
            return {"error": "No directions found for the specified source and destination."}

        leg = directions_result[0]['legs'][0]
        distance = leg['distance']['text']
        duration = leg['duration']['text']

        return {"distance": distance, "duration": duration}
    except Exception as e:
        return {"error": str(e)}

def calculate_travel_time(source, destination, speed):
    try:
        distance_duration_info = get_distance_and_duration(source, destination)
        if "error" in distance_duration_info:
            return distance_duration_info

        # Assuming distance is in kilometers (km) and speed is in km/h
        distance_str = distance_duration_info['distance']
        distance_km = float(distance_str.split()[0])  # Extract the numerical value from the distance string

        predicted_time_hours = distance_km - (distance_km *10/100)

        return {
            "predicted_time_hours": predicted_time_hours
        }
    except Exception as e:
        return {"error": str(e)}

def get_directions(source, destination):
    try:
        directions_result = gmaps.directions(source, destination, mode="driving", departure_time=datetime.now())
        if not directions_result:
            return {"error": "No directions found"}

        return directions_result[0]
    except Exception as e:
        return {"error": str(e)}

def get_lat_lng(address):
    try:
        geocode_result = gmaps.geocode(address)
        if not geocode_result:
            return {"error": "Geocoding failed"}

        location = geocode_result[0]['geometry']['location']
        return location
    except Exception as e:
        return {"error": str(e)}
