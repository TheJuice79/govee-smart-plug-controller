import pytest
from app.time_helpers import is_within_time_window
from datetime import datetime

def test_basic_daytime():
    assert is_within_time_window("08:00", "20:00")

def test_outside_window(monkeypatch):
    from datetime import datetime
    class MockDT(datetime):
        @classmethod
        def now(cls):
            return cls(2024, 1, 1, 2, 0, 0)  # 2 AM
    monkeypatch.setattr("app.time_helpers.datetime", MockDT)
    assert not is_within_time_window("08:00", "20:00")

def test_overnight_window(monkeypatch):
    from datetime import datetime
    class MockDT(datetime):
        @classmethod
        def now(cls):
            return cls(2024, 1, 1, 23, 0, 0)  # 11 PM
    monkeypatch.setattr("app.time_helpers.datetime", MockDT)
    assert is_within_time_window("22:00", "06:00")
    
def test_within_time_window(monkeypatch):
    # Fake current time: 10:00
    fake_now = datetime(2025, 7, 3, 10, 0, 0)

    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fake_now

    monkeypatch.setattr("app.time_helpers.datetime", FakeDateTime)

    assert is_within_time_window("09:00", "18:00") is True
    assert is_within_time_window("20:00", "08:00") is False  # outside overnight window

def test_outside_time_window(monkeypatch):
    # Fake current time: 22:00
    fake_now = datetime(2025, 7, 3, 22, 0, 0)

    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fake_now

    monkeypatch.setattr("app.time_helpers.datetime", FakeDateTime)

    assert is_within_time_window("09:00", "18:00") is False
    assert is_within_time_window("20:00", "06:00") is True  # inside overnight window
