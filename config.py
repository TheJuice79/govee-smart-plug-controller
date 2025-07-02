import os
import sys
import logging

def get_config():
    try:
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
            "CHECK_INTERVAL": float(os.getenv("CHECK_INTERVAL", 15)) * 60
        }
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        sys.exit(1)
