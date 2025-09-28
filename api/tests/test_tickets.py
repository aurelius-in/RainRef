from fastapi.testclient import TestClient
from app import app

def test_tickets_create_list():
    c = TestClient(app)
    r = c.post("/support/tickets", json={"ref_event_id": None, "status": "open"})
    assert r.status_code == 200
    tid = r.json()["id"]
    r2 = c.get("/support/tickets")
    assert r2.status_code == 200
    assert any(it["id"] == tid for it in r2.json().get("items", []))
