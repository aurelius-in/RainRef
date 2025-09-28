from fastapi.testclient import TestClient
from app import app

def test_execute_denied(monkeypatch):
    from services import policy
    async def deny(_):
        return False
    monkeypatch.setattr(policy, "check_allow", deny)
    c = TestClient(app)
    r = c.post("/action/execute", json={"type": "dangerous", "params": {}})
    assert r.status_code == 403
