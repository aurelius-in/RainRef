from fastapi.testclient import TestClient
from app import app

def test_upload_error(monkeypatch):
    from services import blob
    def boom(*a, **k):
        raise Exception("boom")
    monkeypatch.setattr(blob, "upload_bytes", boom)
    c = TestClient(app)
    files = {"file": ("bad.txt", b"oops", "text/plain")}
    r = c.post("/kb/upload", files=files)
    assert r.status_code == 500
