from fastapi.testclient import TestClient
from app import app

def test_signals_emit_and_list():
    c = TestClient(app)
    for i in range(3):
        r = c.post("/signals/emit", json={"origin": f"t:{i}", "type": "friction", "strength": 0.1 * i, "evidence_refs": []})
        assert r.status_code == 200
    r2 = c.get("/signals", params={"page": 1, "limit": 2})
    assert r2.status_code == 200
    assert len(r2.json().get("items", [])) <= 2
