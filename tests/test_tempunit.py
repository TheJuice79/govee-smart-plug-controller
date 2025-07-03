import pytest
from app.config import get_config  # Adjust import to match your structure

def set_required_env(monkeypatch):
    monkeypatch.setenv("GOVEE_API_KEY", "dummy-key")
    monkeypatch.setenv("DEVICE_MAC", "AA:BB:CC:DD:EE:FF")
    monkeypatch.setenv("DEVICE_MODEL", "H5083")
    monkeypatch.setenv("LAT", "44.242")
    monkeypatch.setenv("LON", "-88.278")

def test_valid_temp_unit_fahrenheit(monkeypatch):
    set_required_env(monkeypatch)
    monkeypatch.setenv("TEMP_UNIT", "fahrenheit")
    config = get_config()
    assert config["TEMP_UNIT"] == "fahrenheit"

def test_valid_temp_unit_celsius(monkeypatch):
    set_required_env(monkeypatch)
    monkeypatch.setenv("TEMP_UNIT", "celsius")
    config = get_config()
    assert config["TEMP_UNIT"] == "celsius"

def test_invalid_temp_unit(monkeypatch):
    import pytest  # <-- see next section
    set_required_env(monkeypatch)
    monkeypatch.setenv("TEMP_UNIT", "kelvin")
    with pytest.raises(SystemExit) as e:
        get_config()
    assert e.value.code == 1
