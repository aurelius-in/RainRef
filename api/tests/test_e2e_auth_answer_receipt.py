from fastapi.testclient import TestClient
from app import app


def test_e2e_auth_answer_execute_receipt(monkeypatch):
    client = TestClient(app)

    # Seed ensures admin exists: admin@rainref.local / admin
    # Login
    r = client.post("/auth/login", json={"username": "admin@rainref.local", "password": "admin"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    # Ingest event
    e = client.post("/ref/events", json={"source":"email","channel":"support","text":"I need activation","user_ref":"u-1"})
    assert e.status_code == 200

    # Propose answer
    a = client.post("/support/answer", json={"source":"inbox","channel":"support","text":"I need activation","user_ref":"u-1"})
    assert a.status_code == 200
    data = a.json()
    assert data.get("citations")

    # Execute suggested action (admin JWT required)
    act = {"type": "resend_activation", "params": {"user_id": "u-1"}}
    x = client.post("/action/execute", json=act, headers={"Authorization": f"Bearer {token}"})
    assert x.status_code == 200
    rid = x.json().get("beacon_receipt_id")
    assert rid


