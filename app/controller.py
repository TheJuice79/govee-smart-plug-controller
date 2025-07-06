import requests
import logging
from tenacity import retry, before_log, stop_after_attempt, wait_fixed, retry_if_exception_type
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

class Controller:
    def __init__(self, config):
        self.config = config
        self.current_state = None  # "on", "off", or None

    def turn_on_plug(self):
        self.send_command("on")

    def turn_off_plug(self):
        self.send_command("off")

    @retry(
        wait=wait_fixed(10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(RequestException),
        before=before_log(logger, logging.WARNING)
    )
    def send_command(self, command):
        command = command.lower()
        if self.current_state == command:
            logger.info(f"Plug already {command}. Skipping API call.")
            return

        url = "https://developer-api.govee.com/v1/devices/control"
        headers = {
            "Govee-API-Key": self.config["GOVEE_API_KEY"],
            "Content-Type": "application/json"
        }
        data = {
            "device": self.config["DEVICE_MAC"],
            "model": self.config["DEVICE_MODEL"],
            "cmd": {"name": "turn", "value": command}
        }

        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        logger.info(f"Turned {command} the plug successfully.")
        self.current_state = command  # Cache updated state
