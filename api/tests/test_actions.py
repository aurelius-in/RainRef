import json
from fastapi.testclient import TestClient
from app import app


def test_execute_allowed(monkeypatch):
    # monkeypatch the policy to always allow to keep unit test deterministic
    from services import policy

    async def allow(_):
        return True

    monkeypatch.setattr(policy, "check_allow", allow)

    c = TestClient(app)
    r = c.post("/action/execute", json={"type": "resend_activation", "params": {"user_id": "u1"}})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert "beacon_receipt_id" in body
