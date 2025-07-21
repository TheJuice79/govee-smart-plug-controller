import time
import logging
from datetime import datetime, timedelta

from app.config import get_config
from app.time_helpers import is_within_time_window
from app.controller import Controller
from app.weather import fetch_weather  # ✅ Now imported from weather.py

logger = logging.getLogger(__name__)

def sleep_until_next_start(start_time_str):
    now = datetime.now()
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    start_datetime = datetime.combine(now.date(), start_time)

    if now.time() >= start_time:
        start_datetime += timedelta(days=1)

    sleep_seconds = (start_datetime - now).total_seconds()
    logger.info(f"Outside time window. Sleeping until next START_TIME at {start_datetime.strftime('%Y-%m-%d %H:%M')}")
    time.sleep(sleep_seconds)
    return int(sleep_seconds)

def run_loop():
    config = get_config()
    controller = Controller(config)

    while True:
        if is_within_time_window(config["START_TIME"], config["END_TIME"]):
            temp, cloud = fetch_weather(config["LAT"], config["LON"], config["TEMP_UNIT"], config.get("WEATHERAPI_KEY"))
            if temp is None:
                time.sleep(config["CHECK_INTERVAL"])
                continue

            logger.info(f"Weather: {temp}°, {cloud}% cloud cover")

            if temp >= config["TEMP_THRESHOLD"] and cloud <= config["CLOUD_THRESHOLD"]:
                controller.turn_on_plug()
            else:
                controller.turn_off_plug()

            time.sleep(config["CHECK_INTERVAL"])
        else:
            controller.turn_off_plug(True)
            sleep_until_next_start(config["START_TIME"])
