import pytest
import requests
from datetime import datetime
from app.scheduler import fetch_weather, sleep_until_next_start, run_loop

# --- sleep_until_next_start --------------------------------------------------

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

# --- fetch_weather -----------------------------------------------------------

def test_fetch_weather_success(monkeypatch):
    class FakeResponse:
        def raise_for_status(self): pass
        def json(self):
            return {
                "current": {
                    "temperature_2m": 77.5,
                    "cloudcover": 42
                }
            }

    monkeypatch.setattr("app.scheduler.requests.get", lambda url: FakeResponse())

    temp, cloud = fetch_weather(44.2, -88.3, "fahrenheit")
    assert temp == 77.5
    assert cloud == 42

def test_fetch_weather_failure(monkeypatch, caplog):
    def fake_get(url):
        raise requests.exceptions.RequestException("Fake error")
    monkeypatch.setattr("app.scheduler.requests.get", fake_get)

    temp, cloud = fetch_weather(0, 0, "fahrenheit")
    assert temp is None and cloud is None
    assert "Failed to fetch weather" in caplog.text

# --- run_loop (partial test) --------------------------------------------------

def test_run_loop_outside_time(monkeypatch):
    # mock get_config
    monkeypatch.setattr("app.scheduler.get_config", lambda: {
        "START_TIME": "09:00",
        "END_TIME": "17:00",
        "CHECK_INTERVAL": 1,
    })

    # mock is_within_time_window to always return False
    monkeypatch.setattr("app.scheduler.is_within_time_window", lambda s, e: False)

    # patch sleep_until_next_start to exit after first call
    monkeypatch.setattr("app.scheduler.sleep_until_next_start", lambda s: (_ for _ in ()).throw(SystemExit))

    with pytest.raises(SystemExit):
        run_loop()
