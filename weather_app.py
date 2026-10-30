import requests
import json
from requests.exceptions import RequestException

city = input("Enter city name: ")

try:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if "results" not in data:
        print("City not found!")

    else:
        latitude = data["results"][0]["latitude"]
        longitude = data["results"][0]["longitude"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,weather_code"
        )

        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather = weather_response.json()

        current = weather["current"]

        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            61: "Light rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Light snow",
            80: "Rain showers",
            95: "Thunderstorm"
        }

        code = current["weather_code"]

        print("\n------ WEATHER REPORT ------")
        print("City:", city)
        print("Temperature:", current["temperature_2m"], "°C")
        print("Humidity:", current["relative_humidity_2m"], "%")
        print("Weather Condition:", weather_codes.get(code, "Unknown condition"))

except RequestException:
    print("Error: Unable to connect to the weather service.")

except (KeyError, IndexError, TypeError, ValueError):
    print("Error: Unexpected weather data received.")