import requests
import logging

logger = logging.getLogger(__name__)

def turn_on_plug(config):
    send_command(config, "on")

def turn_off_plug(config):
    send_command(config, "off")

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

    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        logger.info(f"Turned {command} the plug successfully.")
    except requests.RequestException as e:
        logger.error(f"Failed to send {command} command: {e}")
