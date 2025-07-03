import time
import logging
from config import get_config
from time_helpers import is_within_time_window
from controller import turn_on_plug, turn_off_plug
import requests
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)

def fetch_weather(lat, lon, temp_unit):
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,cloudcover"
            f"&temperature_unit={temp_unit}"
            f"&timezone=auto"
        )
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["current"]
        return data["temperature_2m"], data["cloudcover"]
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
    while True:
        now_within_time = is_within_time_window(config["START_TIME"], config["END_TIME"])
        if now_within_time:
            temp, cloud = fetch_weather(config["LAT"], config["LON"], config["TEMP_UNIT"])
            if temp is None:
                time.sleep(config["CHECK_INTERVAL"])
                continue

            logger.info(f"Weather: {temp}°F, {cloud}% cloud cover")

            if temp >= config["TEMP_THRESHOLD"] and cloud <= config["CLOUD_THRESHOLD"]:
                turn_on_plug(config)
            else:
                turn_off_plug(config)

            time.sleep(config["CHECK_INTERVAL"])
        else:
            sleep_until_next_start(config["START_TIME"])