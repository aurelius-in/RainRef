from fastapi.testclient import TestClient
from app import app

def test_action_history(monkeypatch):
    from services import policy
    async def allow(_):
        return True
    monkeypatch.setattr(policy, "check_allow", allow)

    c = TestClient(app)
    c.post("/action/execute", json={"type": "resend_activation", "params": {}})
    r = c.get("/action/history", params={"page": 1, "limit": 1})
    assert r.status_code == 200
    assert len(r.json().get("items", [])) <= 1
