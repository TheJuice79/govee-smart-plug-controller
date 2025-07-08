import pytest
import requests
from app.weather import fetch_weather

def test_fetch_weather_weatherapi(monkeypatch):
    class FakeResponse:
        def raise_for_status(self): pass
        def json(self):
            return {"current": {"temp_f": 78.5, "temp_c": 25.8, "cloud": 60}}

    monkeypatch.setattr("app.weather.requests.get", lambda url: FakeResponse())
    temp, cloud = fetch_weather(44.2, -88.3, "fahrenheit", weatherapi="fake-key")
    assert temp == 78.5
    assert cloud == 60

    temp, cloud = fetch_weather(44.2, -88.3, "celsius", weatherapi="fake-key")
    assert temp == 25.8
    assert cloud == 60

def test_fetch_weather_openmeteo(monkeypatch):
    class FakeResponse:
        def raise_for_status(self): pass
        def json(self):
            return {"current": {"temperature_2m": 77.5, "cloudcover": 42}}

    monkeypatch.setattr("app.weather.requests.get", lambda url: FakeResponse())
    temp, cloud = fetch_weather(44.2, -88.3, "fahrenheit", weatherapi=None)
    assert temp == 77.5
    assert cloud == 42

def test_fetch_weather_failure(monkeypatch, caplog):
    def fake_get(url): raise requests.exceptions.RequestException("API failure")
    monkeypatch.setattr("app.weather.requests.get", fake_get)
    temp, cloud = fetch_weather(44.2, -88.3, "fahrenheit", weatherapi="fake-key")
    assert temp is None and cloud is None
    assert "Failed to fetch weather" in caplog.text