from fastapi.testclient import TestClient
from app import app

def test_signals_delete():
    c = TestClient(app)
    sid = c.post("/signals/emit", json={"origin": "t:X", "type": "noise", "strength": 0.1, "evidence_refs": []}).json()["id"]
    d = c.delete(f"/signals/{sid}")
    assert d.status_code == 200
