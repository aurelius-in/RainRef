from fastapi.testclient import TestClient
from app import app

def test_e2e_answer_and_execute(monkeypatch):
    from services import policy
    async def allow(_):
        return True
    monkeypatch.setattr(policy, "check_allow", allow)

    c = TestClient(app)
    # Seed a KB card
    c.post("/kb/cards", json={"title":"Activation help","body":"Steps to resend activation"})
    # Post an event
    evt = {"source":"email","channel":"support","text":"did not get activation"}
    r_evt = c.post("/ref/events", json=evt)
    assert r_evt.status_code == 200
    # Ask for an answer
    r_ans = c.post("/support/answer", json=evt)
    assert r_ans.status_code == 200
    body = r_ans.json()
    assert body.get("citations")
    # Execute the first suggested action
    act = body.get("actions_suggested", [{}])[0]
    r_exec = c.post("/action/execute", json=act)
    assert r_exec.status_code == 200
    assert r_exec.json().get("beacon_receipt_id")
