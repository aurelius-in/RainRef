from fastapi.testclient import TestClient
from app import app

def test_kb_delete_404():
    c = TestClient(app)
    r = c.delete("/kb/cards/kb-nope")
    assert r.status_code == 404
