import os
import pytest
from app import config
from app.config import get_config

# -- Helpers --

def set_env(env):
    for key, value in env.items():
        os.environ[key] = value

def unset_env(keys):
    for key in keys:
        os.environ.pop(key, None)

# -- Tests --

def test_valid_config(monkeypatch):
    env = {
        "GOVEE_API_KEY": "abc",
        "DEVICE_MAC": "11:22:33:44:55:66",
        "DEVICE_MODEL": "H5083",
        "LAT": "44.0",
        "LON": "-88.0",
        "TEMP_UNIT": "fahrenheit",
    }
    set_env(env)

    cfg = config.get_config()
    assert cfg["TEMP_UNIT"] == "fahrenheit"
    assert cfg["LAT"] == 44.0
    assert cfg["LON"] == -88.0
    unset_env(env)

def test_missing_required(monkeypatch):
    unset_env(["GOVEE_API_KEY", "DEVICE_MAC", "DEVICE_MODEL", "LAT", "LON"])

    with pytest.raises(SystemExit) as e:
        config.get_config()
    assert e.value.code == 1

def test_invalid_temp_unit(monkeypatch):
    env = {
        "GOVEE_API_KEY": "abc",
        "DEVICE_MAC": "11:22:33:44:55:66",
        "DEVICE_MODEL": "H5083",
        "LAT": "44.0",
        "LON": "-88.0",
        "TEMP_UNIT": "kelvin",
    }
    set_env(env)

    with pytest.raises(SystemExit) as e:
        config.get_config()
    assert e.value.code == 1
    unset_env(env)

def test_temp_unit_default(monkeypatch):
    env = {
        "GOVEE_API_KEY": "abc",
        "DEVICE_MAC": "11:22:33:44:55:66",
        "DEVICE_MODEL": "H5083",
        "LAT": "44.0",
        "LON": "-88.0",
    }
    set_env(env)
    os.environ.pop("TEMP_UNIT", None)

    cfg = config.get_config()
    assert cfg["TEMP_UNIT"] == "fahrenheit"
    unset_env(env)

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
