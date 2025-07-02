import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Minimum required environment variables to load controller.py successfully
os.environ["LAT"] = "44.280"
os.environ["LON"] = "-88.292"
os.environ["GOVEE_API_KEY"] = "test"
os.environ["DEVICE_MAC"] = "test"
os.environ["DEVICE_MODEL"] = "H5086"
os.environ["START_TIME"] = "09:00"
os.environ["END_TIME"] = "18:00"
os.environ["TEMP_THRESHOLD"] = "75"
os.environ["CLOUD_THRESHOLD"] = "50"
os.environ["CHECK_INTERVAL"] = "15"

from datetime import datetime, time
from controller import is_within_time_window

# Setup environment for test
os.environ["START_TIME"] = "09:00"
os.environ["END_TIME"] = "18:00"

def test_time_within_window(monkeypatch):
    class MockDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.combine(datetime.today(), time(10, 0))
    monkeypatch.setattr("controller.datetime", MockDateTime)
    assert is_within_time_window()

def test_time_outside_window(monkeypatch):
    class MockDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.combine(datetime.today(), time(6, 0))
    monkeypatch.setattr("controller.datetime", MockDateTime)
    assert not is_within_time_window()
