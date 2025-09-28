from fastapi.testclient import TestClient
from app import app

def test_events_pagination():
    c = TestClient(app)
    for i in range(3):
        c.post("/ref/events", json={"source":"email","channel":"support","text":f"hello {i}"})
    r = c.get("/ref/events", params={"page": 1, "limit": 2})
    assert r.status_code == 200
    assert len(r.json().get("items", [])) <= 2


def test_kb_update_delete():
    c = TestClient(app)
    r = c.post("/kb/cards", json={"title":"Old","body":"Body"})
    cid = r.json()["id"]
    r2 = c.put(f"/kb/cards/{cid}", json={"title":"New"})
    assert r2.status_code == 200
    r3 = c.get(f"/kb/cards/{cid}")
    assert r3.json()["title"] == "New"
    r4 = c.delete(f"/kb/cards/{cid}")
    assert r4.status_code == 200
    r5 = c.get(f"/kb/cards/{cid}")
    assert r5.status_code == 404
