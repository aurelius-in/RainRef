from fastapi.testclient import TestClient
from app import app


def test_export_requires_key(monkeypatch):
    from config import settings
    monkeypatch.setattr(settings, "api_key", "secret")
    c = TestClient(app)
    r = c.get("/ref/events/export")
    assert r.status_code == 401
    r2 = c.get("/ref/events/export", headers={"X-API-Key":"secret"})
    assert r2.status_code == 200
