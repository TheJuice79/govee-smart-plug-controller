import pytest
from time_helpers import is_within_time_window

def test_basic_daytime():
    assert is_within_time_window("08:00", "20:00")

def test_outside_window(monkeypatch):
    from datetime import datetime
    class MockDT(datetime):
        @classmethod
        def now(cls):
            return cls(2024, 1, 1, 2, 0, 0)  # 2 AM
    monkeypatch.setattr("time_helpers.datetime", MockDT)
    assert not is_within_time_window("08:00", "20:00")

def test_overnight_window(monkeypatch):
    from datetime import datetime
    class MockDT(datetime):
        @classmethod
        def now(cls):
            return cls(2024, 1, 1, 23, 0, 0)  # 11 PM
    monkeypatch.setattr("time_helpers.datetime", MockDT)
    assert is_within_time_window("22:00", "06:00")
