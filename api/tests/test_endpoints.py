from fastapi.testclient import TestClient
from app import app

def test_events_list_and_get(monkeypatch):
    c = TestClient(app)
    r = c.post("/ref/events", json={"source":"email","channel":"support","text":"hello"})
    assert r.status_code == 200
    eid = r.json()["id"]
    r2 = c.get("/ref/events")
    assert r2.status_code == 200
    assert any(it["id"] == eid for it in r2.json().get("items", []))
    r3 = c.get(f"/ref/events/{eid}")
    assert r3.status_code == 200
    assert r3.json()["id"] == eid

def test_kb_get_by_id():
    c = TestClient(app)
    r = c.post("/kb/cards", json={"title":"T","body":"B"})
    cid = r.json()["id"]
    r2 = c.get(f"/kb/cards/{cid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == cid
