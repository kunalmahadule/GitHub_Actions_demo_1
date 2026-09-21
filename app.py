from flask import Flask, render_template, request
import requests

app = Flask(__name__)

### Handle invalid city name issue resolved here
def get_city_coordinates(city):
    """Find latitude and longitude for a city."""

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()

        if not data.get("results"):
            return None

        location = data["results"][0]

        return {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "name": location.get("name"),
            "country": location.get("country"),
            "admin1": location.get("admin1")
        }

    except requests.RequestException:
        return None


def get_weather(latitude, longitude):
    """Get current weather information."""

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "auto"
    }

    try:
        response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()

        current = data.get("current")

        if not current:
            return None

        return {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "weather_code": current.get("weather_code")
        }

    except requests.RequestException:
        return None


@app.route("/", methods=["GET", "POST"])
def home():

    city = None
    temperature = None
    humidity = None
    wind_speed = None
    weather_code = None
    country = None
    error = None

    if request.method == "POST":

        city = request.form.get("city", "").strip()

        # Validate city
        if not city:
            error = "Please enter a city name."

        else:
            location = get_city_coordinates(city)

            if not location:
                error = "City not found or geocoding service unavailable."

            else:
                country = location["country"]

                weather = get_weather(
                    location["latitude"],
                    location["longitude"]
                )

                if not weather:
                    error = "Unable to get weather information."

                else:
                    temperature = weather["temperature"]
                    humidity = weather["humidity"]
                    wind_speed = weather["wind_speed"]
                    weather_code = weather["weather_code"]

    return render_template(
        "index.html",
        city=city,
        country=country,
        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
        weather_code=weather_code,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True, port=5005)
