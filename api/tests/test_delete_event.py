from fastapi.testclient import TestClient
from app import app

def test_delete_event():
    c = TestClient(app)
    r = c.post("/ref/events", json={"source":"email","channel":"support","text":"to delete"})
    eid = r.json()["id"]
    d = c.delete(f"/ref/events/{eid}")
    assert d.status_code == 200
    g = c.get(f"/ref/events/{eid}")
    assert g.status_code == 404
