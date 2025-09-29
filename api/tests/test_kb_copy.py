from fastapi.testclient import TestClient
from app import app

def test_kb_copy_new_id():
    c = TestClient(app)
    r = c.post("/kb/cards", json={"title": "CopyMe", "body": "B"})
    cid = r.json()["id"]
    r2 = c.post(f"/kb/cards/{cid}/copy")
    assert r2.status_code == 200
    new_id = r2.json()["id"]
    assert new_id != cid
    r3 = c.get(f"/kb/cards/{new_id}")
    assert r3.status_code == 200
