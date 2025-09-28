from fastapi.testclient import TestClient
from app import app

def test_ref_filters():
    c = TestClient(app)
    c.post("/ref/events", json={"source":"email","channel":"support","text":"hello filters"})
    r = c.get("/ref/events", params={"source":"email","channel":"support","q":"hello"})
    assert r.status_code == 200
    items = r.json().get("items", [])
    assert any("hello" in (it.get("text") or "") for it in items)
