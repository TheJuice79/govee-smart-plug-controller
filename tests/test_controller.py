import pytest
from controller import send_command

def test_send_command_mocked(monkeypatch):
    class MockResponse:
        def raise_for_status(self): pass

    def mock_put(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("controller.requests.put", mock_put)

    config = {
        "DEVICE_MAC": "mock-mac",
        "DEVICE_MODEL": "mock-model",
        "GOVEE_API_KEY": "mock-key"
    }

    try:
        send_command(config, True)
        send_command(config, False)
    except Exception:
        pytest.fail("send_command raised unexpectedly")
