from fastapi.testclient import TestClient
from app import app

def test_ticket_update():
    c = TestClient(app)
    r = c.post("/support/tickets", json={"status": "open"})
    tid = r.json()["id"]
    r2 = c.put(f"/support/tickets/{tid}", json={"status": "closed"})
    assert r2.status_code == 200
    assert r2.json()["status"] == "closed"
