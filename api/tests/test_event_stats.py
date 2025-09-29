from fastapi.testclient import TestClient
from app import app

def test_event_stats():
    c = TestClient(app)
    c.post("/ref/events", json={"source":"email","channel":"support","text":"hi"})
    r = c.get("/ref/events/stats")
    assert r.status_code == 200
    assert "by_channel" in r.json()
