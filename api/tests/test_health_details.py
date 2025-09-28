from fastapi.testclient import TestClient
from app import app

def test_health_details():
    c = TestClient(app)
    r = c.get("/healthz/details")
    assert r.status_code == 200
    body = r.json()
    assert "db" in body and "opa" in body
