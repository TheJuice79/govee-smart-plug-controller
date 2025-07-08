import pytest
import requests
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.scheduler import sleep_until_next_start, run_loop

def test_sleep_until_next_start_after(monkeypatch):
    fake_now = datetime(2025, 7, 3, 22, 30)
    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None): return fake_now

    monkeypatch.setattr("app.scheduler.datetime", FakeDateTime)
    sleep_called = []
    monkeypatch.setattr("app.scheduler.time.sleep", lambda s: sleep_called.append(s))
    result = sleep_until_next_start("09:00")
    assert abs(result - 37800) < 1
    assert sleep_called[0] == result

def test_sleep_until_next_start_before(monkeypatch):
    fake_now = datetime(2025, 7, 3, 6, 30)
    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None): return fake_now

    monkeypatch.setattr("app.scheduler.datetime", FakeDateTime)
    sleep_called = []
    monkeypatch.setattr("app.scheduler.time.sleep", lambda s: sleep_called.append(s))
    result = sleep_until_next_start("09:00")
    assert abs(result - 9000) < 1
    assert sleep_called[0] == result

def test_run_loop_outside_time(monkeypatch):
    monkeypatch.setattr("app.scheduler.get_config", lambda: {
        "START_TIME": "09:00",
        "END_TIME": "17:00",
        "CHECK_INTERVAL": 1,
        "LAT": 0,
        "LON": 0,
        "TEMP_UNIT": "fahrenheit",
        "TEMP_THRESHOLD": 75,
        "CLOUD_THRESHOLD": 50,
        "WEATHERAPI_KEY": None
    })
    monkeypatch.setattr("app.scheduler.is_within_time_window", lambda s, e: False)
    monkeypatch.setattr("app.scheduler.sleep_until_next_start", lambda s: (_ for _ in ()).throw(SystemExit))

    with patch("app.scheduler.Controller") as MockController:
        mock_controller = MagicMock()
        MockController.return_value = mock_controller
        with pytest.raises(SystemExit):
            run_loop()
        mock_controller.turn_off_plug.assert_called_once()