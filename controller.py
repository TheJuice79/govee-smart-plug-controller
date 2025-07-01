import requests
import logging
import os
import time
import signal
import sys
from datetime import datetime

# Configure logging format and level
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

logger.info(f"Govee controller starting up...{datetime.now()}")

# Load config from environment variables set by Docker/Portainer
GOVEE_API_KEY = os.getenv("GOVEE_API_KEY")
DEVICE_MAC = os.getenv("DEVICE_MAC")
DEVICE_MODEL = os.getenv("DEVICE_MODEL")
LAT = float(os.getenv("LAT"))
LON = float(os.getenv("LON"))
TEMP_THRESHOLD = float(os.getenv("TEMP_THRESHOLD", 75))    # Temperature threshold in °F (Default 75°F)
CLOUD_THRESHOLD = float(os.getenv("CLOUD_THRESHOLD", 50))  # Cloud cover threshold in % (Default 50%)
CHECK_INTERVAL = float(os.getenv("CHECK_INTERVAL", 15)) * 60  # Time between checks in seconds (Default 15 min)

def graceful_shutdown(signum, frame):
    """
    Handle shutdown signals by turning off the smart plug before exiting.
    """
    logger.info(f"Received signal {signum}, turning off plug before exit...")
    try:
        control_govee(False)
    except Exception as e:
        logger.error(f"Error turning off plug during shutdown: {e}")
    sys.exit(0)

def get_temperature():
    """
    Fetch current temperature (°F) from open-meteo.com for the configured latitude and longitude.
    Returns temperature as a float, or None if error occurs or data is missing.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        f"&current_weather=true"
        f"&temperature_unit=fahrenheit"
        f"&timezone=auto"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        temp = data.get("current_weather", {}).get("temperature")
        if temp is None:
            logger.warning("Temperature data missing in weather API response")
        return temp
    except Exception as e:
        logger.error(f"Failed to get temperature: {e}")
        return None

def get_cloud_cover():
    """
    Fetch current cloud cover (%) from open-meteo.com for the configured latitude and longitude.
    Returns cloud cover as a float, or None if error occurs or data is missing.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        f"&current=cloud_cover"
        f"&timezone=auto"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        cloud_cover = data.get("current", {}).get("cloud_cover")
        if cloud_cover is None:
            logger.warning("Cloud cover data missing in weather API response")
        return cloud_cover
    except Exception as e:
        logger.error(f"Failed to get cloud cover: {e}")
        return None

def control_govee(turn_on: bool):
    """
    Send command to Govee smart plug to turn it ON or OFF.
    Logs the HTTP response status and response text.
    """
    url = "https://developer-api.govee.com/v1/devices/control"
    payload = {
        "device": DEVICE_MAC,
        "model": DEVICE_MODEL,
        "cmd": {
            "name": "turn",
            "value": "on" if turn_on else "off"
        }
    }
    headers = {
        "Govee-API-Key": GOVEE_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        res = requests.put(url, json=payload, headers=headers, timeout=10)
        logger.info(f"Sent command: {'ON' if turn_on else 'OFF'} (status {res.status_code})")
        logger.info(res.text)
    except Exception as e:
        logger.error(f"Failed to send control command to Govee device: {e}")

def should_be_on(temp, clouds):
    """
    Determine if the smart plug should be ON based on temperature and cloud cover thresholds.
    Returns True if temp is above TEMP_THRESHOLD and cloud cover is below CLOUD_THRESHOLD.
    """
    if temp is None or clouds is None:
        # If either value is None, assume plug should be OFF for safety
        return False
    return temp > TEMP_THRESHOLD and clouds < CLOUD_THRESHOLD

def main():
    """
    Main control loop:
    - Runs continuously.
    - Checks weather and controls plug every CHECK_INTERVAL seconds between 9AM and 6PM.
    - Turns plug OFF after 6PM and sleeps until 9AM next day.
    - Sleeps until 9AM if run before 9AM.
    """
    # Register signal handlers to catch termination and cleanup
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    plug_is_on = None
    logger.info("Starting Govee controller loop...")
    logger.info(
        f"Loaded environment variables: "
        f"GOVEE_API_KEY={'***' if GOVEE_API_KEY else 'Not Set'}, "
        f"DEVICE_MAC={DEVICE_MAC}, "
        f"DEVICE_MODEL={DEVICE_MODEL}, "
        f"LAT={LAT}, "
        f"LON={LON}, "
        f"TEMP_THRESHOLD={TEMP_THRESHOLD}, "
        f"CLOUD_THRESHOLD={CLOUD_THRESHOLD}, "
        f"CHECK_INTERVAL={CHECK_INTERVAL} seconds"
    )

    while True:
        now = datetime.now()
        hour = now.hour

        if 9 <= hour < 18:
            # During active hours, check weather and control plug accordingly
            try:
                temp = get_temperature()
                clouds = get_cloud_cover()
                logger.info(f"Temp: {temp}°F, Cloud Cover: {clouds}%")

                if should_be_on(temp, clouds):
                    if plug_is_on is not True:
                        control_govee(True)
                        plug_is_on = True
                    else:
                        logger.info("Plug already ON, no change.")
                else:
                    if plug_is_on is not False:
                        control_govee(False)
                        plug_is_on = False
                    else:
                        logger.info("Plug already OFF, no change.")

            except Exception as e:
                logger.error(f"Error checking weather or controlling device: {e}")

            # Log plug state and sleep before next check
            state_str = "ON" if plug_is_on is True else "OFF" if plug_is_on is False else "UNKNOWN"
            logger.info(f"Plug is {state_str}. Sleeping for {CHECK_INTERVAL} seconds.")
            time.sleep(CHECK_INTERVAL)

        elif hour >= 18:
            # After 6PM, ensure plug is OFF and sleep until 9AM next day
            if plug_is_on != False:
                logger.info("It's after 6PM. Turning off plug.")
                control_govee(False)
                plug_is_on = False
            tomorrow = now.replace(hour=9, minute=0, second=0, microsecond=0)
            if now.hour >= 18:
                # handle day overflow (not perfect on month end, consider dateutil for production)
                try:
                    tomorrow = tomorrow.replace(day=now.day + 1)
                except ValueError:
                    # fallback for month end - just add 1 day with timedelta (import timedelta if used)
                    from datetime import timedelta
                    tomorrow = tomorrow + timedelta(days=1)
                    tomorrow = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
            sleep_seconds = (tomorrow - now).total_seconds()
            logger.info(f"Sleeping until 9:00 AM tomorrow ({int(sleep_seconds)} seconds)...")
            time.sleep(sleep_seconds)

        else:
            # Before 9AM, sleep until 9AM
            sleep_seconds = (now.replace(hour=9, minute=0, second=0, microsecond=0) - now).total_seconds()
            logger.info(f"Too early. Sleeping until 9:00 AM ({int(sleep_seconds)} seconds)...")
            time.sleep(sleep_seconds)

if __name__ == "__main__":
    main()
