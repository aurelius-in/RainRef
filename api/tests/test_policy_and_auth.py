from fastapi.testclient import TestClient
from app import app


def test_action_denied_reason(monkeypatch):
    from services import policy

    async def deny_missing_user(_action, user=None):
        return {"allow": False, "reason": "policy: missing user_ref"}

    monkeypatch.setattr(policy, "check_allow", deny_missing_user)

    c = TestClient(app)
    r = c.post("/action/execute", json={"type": "resend_activation", "params": {}})
    assert r.status_code == 403
    assert "missing user_ref" in r.json().get("detail", "")


def test_support_endpoints_require_role(monkeypatch):
    from config import settings
    # Enable gating via existing flag
    monkeypatch.setattr(settings, "require_jwt_for_admin", True)

    c = TestClient(app)
    # No bearer token
    r = c.post("/support/answer", json={"source": "inbox", "channel": "support", "text": "hi"})
    assert r.status_code == 401


