from fastapi.testclient import TestClient
from app import app

def test_rate_limit_settings(monkeypatch):
    from config import settings
    monkeypatch.setattr(settings, "rate_limit_window_sec", 5)
    monkeypatch.setattr(settings, "rate_limit_per_window", 1)

    from services import policy
    async def allow(_):
        return True
    monkeypatch.setattr(policy, "check_allow", allow)

    c = TestClient(app)
    payload = {"type": "resend_activation", "params": {}}
    assert c.post("/action/execute", json=payload).status_code == 200
    assert c.post("/action/execute", json=payload).status_code == 429
