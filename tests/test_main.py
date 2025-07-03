import pytest
import signal
from app import main

def test_shutdown(monkeypatch):
    called = {}

    def fake_exit(code):
        called["exit"] = code
        raise SystemExit(code)

    monkeypatch.setattr("sys.exit", fake_exit)

    with pytest.raises(SystemExit) as e:
        main.shutdown(signal.SIGTERM, None)

    assert e.value.code == 0
    assert called["exit"] == 0