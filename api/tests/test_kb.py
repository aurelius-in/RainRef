from fastapi.testclient import TestClient
from app import app

def test_kb_upsert_and_search(monkeypatch):
    c = TestClient(app)
    r = c.post("/kb/cards", json={"title": "Activation", "body": "How to resend activation.", "tags": ["activation"]})
    assert r.status_code == 200
    cid = r.json()["id"]
    r2 = c.get("/kb/cards", params={"query": "activation"})
    assert r2.status_code == 200
    assert any(item["id"] == cid for item in r2.json()["results"])

def test_upload_route(monkeypatch):
    from services import blob
    monkeypatch.setattr(blob, "upload_bytes", lambda container, name, data, content_type: "http://local/blob")
    c = TestClient(app)
    files = {"file": ("guide.txt", b"hello", "text/plain")}
    r = c.post("/kb/upload", files=files)
    assert r.status_code == 200
    assert r.json()["url"].startswith("http")
