import requests
import logging
from tenacity import retry, before_log, stop_after_attempt, wait_fixed, retry_if_exception_type
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def turn_on_plug(config):
    send_command(config, "on")

def turn_off_plug(config):
    send_command(config, "off")

@retry(
    wait=wait_fixed(10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(RequestException),
    before=before_log(logger, logging.WARNING)
)
def send_command(config, command):
    url = "https://developer-api.govee.com/v1/devices/control"
    headers = {
        "Govee-API-Key": config["GOVEE_API_KEY"],
        "Content-Type": "application/json"
    }
    data = {
        "device": config["DEVICE_MAC"],
        "model": config["DEVICE_MODEL"],
        "cmd": {"name": "turn", "value": command}
    }

    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    logger.info(f"Turned {command} the plug successfully.")
