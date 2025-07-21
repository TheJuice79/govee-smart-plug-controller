import requests
import logging

logger = logging.getLogger(__name__)

def fetch_weather(lat, lon, temp_unit, weatherapi):
    try:
        if temp_unit.lower() not in ("fahrenheit", "celsius"):
            raise ValueError("Invalid temp_unit. Use 'fahrenheit' or 'celsius'.")

        is_fahrenheit = temp_unit.lower() == "fahrenheit"

        if weatherapi:
            # --- WeatherAPI branch ---
            url = (
                f"https://api.weatherapi.com/v1/current.json"
                f"?key={weatherapi}"
                f"&q={lat},{lon}"
                f"&aqi=no"
            )
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()["current"]

                temperature = data["temp_f"] if is_fahrenheit else data["temp_c"]
                cloud = data["cloud"]

            except:
                logger.warning("WeatherAPI request failed, falling back to Open-Meteo.")
                fetch_weather(lat, lon, temp_unit, None)  # Retry without WeatherAPI

        else:
            # --- Open-Meteo fallback ---
            unit_param = "fahrenheit" if is_fahrenheit else "celsius"
            url = (
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={lat}&longitude={lon}"
                f"&current=temperature_2m,cloudcover"
                f"&temperature_unit={unit_param}"
                f"&timezone=auto"
            )

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()["current"]

            temperature = data["temperature_2m"]
            cloud = data["cloudcover"]

        return temperature, cloud

    except Exception as e:
        logger.error(f"Failed to fetch weather: {e}")
        return None, None
