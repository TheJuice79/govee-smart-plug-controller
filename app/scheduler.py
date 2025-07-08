import time
import logging
from app.config import get_config
from app.time_helpers import is_within_time_window
from app.controller import Controller
import requests
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)

def fetch_weather(lat, lon, temp_unit, weatherapi):
    try:
        # Ensure valid TEMP_UNIT for WeatherAPI ('f' or 'c')
        if temp_unit.lower() not in ("fahrenheit", "celsius"):
            raise ValueError("Invalid temp_unit. Use 'fahrenheit' or 'celsius'.")

        # WeatherAPI uses 'f' or 'c' in query param
        is_fahrenheit = temp_unit.lower() == "fahrenheit"
        query_unit = "yes" if is_fahrenheit else "no"

        api_key = weatherapi
        if not api_key:
            raise EnvironmentError("Missing WEATHERAPI_KEY environment variable.")

        url = (
            f"https://api.weatherapi.com/v1/current.json"
            f"?key={api_key}"
            f"&q={lat},{lon}"
            f"&aqi=no"
        )

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["current"]

        temperature = data["temp_f"] if is_fahrenheit else data["temp_c"]
        cloud = data["cloud"]  # Percentage (0–100)

        return temperature, cloud

    except Exception as e:
        logger.error(f"Failed to fetch weather: {e}")
        return None, None


def sleep_until_next_start(start_time_str):
    # Compute sleep duration until next START_TIME
    now = datetime.now()
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    start_datetime = datetime.combine(now.date(), start_time)

    if now.time() >= start_time:
        # It's past today's START_TIME, so wait until tomorrow's
        start_datetime += timedelta(days=1)

    sleep_seconds = (start_datetime - now).total_seconds()
    logger.info(f"Outside time window. Sleeping until next START_TIME at {start_datetime.strftime('%Y-%m-%d %H:%M')}")
    time.sleep(sleep_seconds)
    return int(sleep_seconds)  # for test visibility

def run_loop():
    config = get_config()
    controller = Controller(config)  # ✅ instantiate the class

    while True:
        now_within_time = is_within_time_window(config["START_TIME"], config["END_TIME"])
        if now_within_time:
            temp, cloud = fetch_weather(config["LAT"], config["LON"], config["TEMP_UNIT"], config["WEATHERAPI_KEY"])
            if temp is None:
                time.sleep(config["CHECK_INTERVAL"])
                continue

            logger.info(f"Weather: {temp}°F, {cloud}% cloud cover")

            if temp >= config["TEMP_THRESHOLD"] and cloud <= config["CLOUD_THRESHOLD"]:
                controller.turn_on_plug()
            else:
                controller.turn_off_plug()

            time.sleep(config["CHECK_INTERVAL"])
        else:
            controller.turn_off_plug()
            sleep_until_next_start(config["START_TIME"])