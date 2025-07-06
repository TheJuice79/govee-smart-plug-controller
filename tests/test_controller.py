import pytest
from app.controller import Controller

def test_send_command_mocked(monkeypatch):
    class MockResponse:
        def raise_for_status(self): pass

    def mock_put(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("app.controller.requests.put", mock_put)

    config = {
        "DEVICE_MAC": "mock-mac",
        "DEVICE_MODEL": "mock-model",
        "GOVEE_API_KEY": "mock-key"
    }

    controller = Controller(config)  # ✅ Create instance

    try:
        controller.send_command("on")   # ✅ Call instance method
        controller.send_command("off")
    except Exception:
        pytest.fail("send_command raised unexpectedly")
