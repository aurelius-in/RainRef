from fastapi.testclient import TestClient
from app import app

def test_metrics_basic():
    c = TestClient(app)
    r = c.get("/metrics/basic")
    assert r.status_code == 200
    body = r.json()
    assert "uptime_seconds" in body and "requests_total" in body
