from fastapi.testclient import TestClient
from app import app

def test_ticket_actions_listing(monkeypatch):
    from services import policy
    async def allow(_):
        return True
    monkeypatch.setattr(policy, "check_allow", allow)

    c = TestClient(app)
    t = c.post("/support/tickets", json={"status": "open"}).json()["id"]
    c.post("/action/execute", json={"type": "note", "ticket_id": t, "params": {"msg": "hi"}})
    r = c.get(f"/support/tickets/{t}/actions")
    assert r.status_code == 200
    items = r.json().get("items", [])
    assert any(it["type"] == "note" for it in items)
