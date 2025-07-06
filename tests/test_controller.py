import pytest
from app.controller import Controller

@pytest.fixture
def controller_with_mock(monkeypatch):
    call_log = []

    class MockResponse:
        def raise_for_status(self): pass

    def mock_put(*args, **kwargs):
        call_log.append(kwargs["json"]["cmd"]["value"])
        return MockResponse()

    monkeypatch.setattr("app.controller.requests.put", mock_put)

    config = {
        "DEVICE_MAC": "mock-mac",
        "DEVICE_MODEL": "mock-model",
        "GOVEE_API_KEY": "mock-key"
    }

    controller = Controller(config)
    return controller, call_log

def test_send_command_on_sets_state_and_calls_api(controller_with_mock):
    controller, call_log = controller_with_mock

    controller.send_command("on")

    assert controller.current_state == "on"
    assert call_log == ["on"]

def test_redundant_command_does_not_call_api(controller_with_mock):
    controller, call_log = controller_with_mock

    controller.send_command("on")
    controller.send_command("on")  # Should not trigger another call

    assert call_log == ["on"]

def test_switching_state_calls_api(controller_with_mock):
    controller, call_log = controller_with_mock

    controller.send_command("on")
    controller.send_command("off")

    assert controller.current_state == "off"
    assert call_log == ["on", "off"]

def test_redundant_off_command_does_not_call_api(controller_with_mock):
    controller, call_log = controller_with_mock

    controller.send_command("off")
    controller.send_command("off")  # Should not re-call

    assert call_log == ["off"]

def test_invalid_command_is_ignored(controller_with_mock):
    controller, call_log = controller_with_mock

    controller.send_command("banana")  # Invalid
    assert controller.current_state is None
    assert call_log == []  # No API call made

def test_command_is_case_insensitive(controller_with_mock):
    controller, call_log = controller_with_mock

    controller.send_command("ON")
    assert controller.current_state == "on"
    assert call_log == ["on"]

from requests.exceptions import RequestException

def test_request_exception_does_not_update_state(monkeypatch):
    def mock_put(*args, **kwargs):
        raise RequestException("Network error")

    monkeypatch.setattr("app.controller.requests.put", mock_put)

    config = {
        "DEVICE_MAC": "mock-mac",
        "DEVICE_MODEL": "mock-model",
        "GOVEE_API_KEY": "mock-key"
    }

    controller = Controller(config)
    controller.current_state = "off"  # Pretend we're already off

    controller.send_command("on")  # Will raise internally

    assert controller.current_state == "off"  # Should not change

def test_initial_state_none_transitions_on(controller_with_mock):
    controller, call_log = controller_with_mock

    assert controller.current_state is None

    controller.send_command("on")
    assert controller.current_state == "on"
    assert call_log == ["on"]

@pytest.mark.parametrize("cmd", ["on", "ON", "On"])
def test_case_insensitivity(cmd, controller_with_mock):
    controller, call_log = controller_with_mock
    controller.send_command(cmd)
    assert controller.current_state == "on"
    assert call_log == ["on"]

def test_class_method_call_raises_error():
    config = {
        "DEVICE_MAC": "mock-mac",
        "DEVICE_MODEL": "mock-model",
        "GOVEE_API_KEY": "mock-key"
    }

    with pytest.raises(AttributeError):
        Controller.turn_off_plug(config)  # ❌ Misuse: passing dict to instance method