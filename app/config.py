# config.py
import os
import sys
import logging

def get_config():
    required = ["GOVEE_API_KEY", "DEVICE_MAC", "DEVICE_MODEL", "LAT", "LON"]
    for var in required:
        if os.getenv(var) is None:
            print(f"Missing required environment variable: {var}")
            sys.exit(1)

    return {
        "GOVEE_API_KEY": os.getenv("GOVEE_API_KEY"),
        "DEVICE_MAC": os.getenv("DEVICE_MAC"),
        "DEVICE_MODEL": os.getenv("DEVICE_MODEL"),
        "LAT": float(os.getenv("LAT")),
        "LON": float(os.getenv("LON")),
        "START_TIME": os.getenv("START_TIME", "00:00"),
        "END_TIME": os.getenv("END_TIME", "23:59"),
        "TEMP_THRESHOLD": float(os.getenv("TEMP_THRESHOLD", 75)),
        "CLOUD_THRESHOLD": float(os.getenv("CLOUD_THRESHOLD", 50)),
        "CHECK_INTERVAL": float(os.getenv("CHECK_INTERVAL", 15)) * 60,
    }

# Optional log-to-file support
logger = logging.getLogger(__name__)
if os.getenv("LOG_TO_FILE") == "1":
    file_handler = logging.FileHandler("controller.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
