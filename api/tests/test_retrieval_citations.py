from fastapi.testclient import TestClient
from app import app

def test_retrieval_returns_citations():
    c = TestClient(app)
    c.post("/kb/cards", json={"title":"Reset password","body":"To reset password, click the reset link"})
    r = c.post("/support/answer", json={"source":"email","channel":"support","text":"How to reset password?"})
    assert r.status_code == 200
    assert len(r.json().get("citations", [])) >= 1
