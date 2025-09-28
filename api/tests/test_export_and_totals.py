from fastapi.testclient import TestClient
from app import app

def test_events_export_and_totals():
    c = TestClient(app)
    for i in range(2):
        c.post("/ref/events", json={"source":"email","channel":"support","text":f"hello {i}"})
    r = c.get("/ref/events", params={"page":1, "limit":1})
    assert r.status_code == 200
    assert "total" in r.json()
    rx = c.get("/ref/events/export")
    assert rx.status_code == 200
    assert rx.headers.get("content-type", "").startswith("text/csv")
