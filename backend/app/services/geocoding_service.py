from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ecolens", timeout=10)

def get_coordinates(city_name):
    """Convert a city name into latitude and longitude."""
    try:
        location = geolocator.geocode(city_name)
        if location:
            return {
                "city": city_name,
                "latitude": location.latitude,
                "longitude": location.longitude
            }
        return {"error": "City not found"}
    except Exception:
        return {"error": "Geocoding service unavailable"}