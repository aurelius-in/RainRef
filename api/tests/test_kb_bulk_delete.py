from fastapi.testclient import TestClient
from app import app

def test_kb_bulk_delete():
    c = TestClient(app)
    a = c.post("/kb/cards", json={"title": "A", "body": "x"}).json()["id"]
    b = c.post("/kb/cards", json={"title": "B", "body": "y"}).json()["id"]
    r = c.post("/kb/cards/delete", json={"ids": [a, b]})
    assert r.status_code == 200
