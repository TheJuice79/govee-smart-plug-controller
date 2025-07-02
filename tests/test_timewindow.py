import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
