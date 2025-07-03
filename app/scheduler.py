import time
import logging
from config import get_config
from time_helpers import is_within_time_window
from controller import turn_on_plug, turn_off_plug
import requests

logger = logging.getLogger(__name__)

def fetch_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,cloudcover&timezone=auto"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["current"]
        return data["temperature_2m"], data["cloudcover"]
    except Exception as e:
        logger.error(f"Failed to fetch weather: {e}")
        return None, None

def run_loop():
    config = get_config()
    while True:
        now_within_time = is_within_time_window(config["START_TIME"], config["END_TIME"])
        if now_within_time:
            temp, cloud = fetch_weather(config["LAT"], config["LON"])
            if temp is None:
                time.sleep(config["CHECK_INTERVAL"])
                continue

            logger.info(f"Weather: {temp}°F, {cloud}% cloud cover")

            if temp >= config["TEMP_THRESHOLD"] and cloud <= config["CLOUD_THRESHOLD"]:
                turn_on_plug(config)
            else:
                turn_off_plug(config)
        else:
            logger.info("Outside active hours, skipping control.")
        time.sleep(config["CHECK_INTERVAL"])
