from typing import Any, Dict, Optional
import requests

class RainRefClient:
    def __init__(self, base_url: str = "http://localhost:8080", token: Optional[str] = None) -> None:
        self.base_url = base_url.rstrip('/')
        self._s = requests.Session()
        if token:
            self.set_token(token)

    def set_token(self, token: str) -> None:
        self._s.headers.update({"Authorization": f"Bearer {token}"})

    def login(self, username: str, password: str) -> Dict[str, Any]:
        r = self._s.post(f"{self.base_url}/auth/login", json={"username": username, "password": password})
        r.raise_for_status()
        data = r.json()
        tok = data.get("access_token")
        if tok:
            self.set_token(tok)
        return data

    def whoami(self) -> Dict[str, Any]:
        r = self._s.get(f"{self.base_url}/auth/whoami")
        r.raise_for_status()
        return r.json()

    def health(self) -> Dict[str, Any]:
        r = self._s.get(f"{self.base_url}/healthz")
        r.raise_for_status()
        return r.json()

    def list_events(self) -> Dict[str, Any]:
        r = self._s.get(f"{self.base_url}/ref/events")
        r.raise_for_status()
        return r.json()

    def ingest_event(self, source: str, channel: str, text: str, user_ref: Optional[str] = None) -> Dict[str, Any]:
        payload = {"source": source, "channel": channel, "text": text}
        if user_ref:
            payload["user_ref"] = user_ref
        r = self._s.post(f"{self.base_url}/ref/events", json=payload)
        r.raise_for_status()
        return r.json()

    def propose_answer(self, text: str, source: str = "inbox", channel: str = "support", user_ref: Optional[str] = None) -> Dict[str, Any]:
        payload = {"source": source, "channel": channel, "text": text}
        if user_ref:
            payload["user_ref"] = user_ref
        r = self._s.post(f"{self.base_url}/support/answer", json=payload)
        r.raise_for_status()
        return r.json()

    def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        r = self._s.post(f"{self.base_url}/action/execute", json=action)
        r.raise_for_status()
        return r.json()

    def get_receipt(self, receipt_id: str) -> Dict[str, Any]:
        r = self._s.get(f"{self.base_url}/audit/{receipt_id}")
        r.raise_for_status()
        return r.json()

    def list_actions_by_type(self, type: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        r = self._s.get(f"{self.base_url}/action/history/by-type", params={"type": type, "page": page, "limit": limit})
        r.raise_for_status()
        return r.json()

    def delete_signal(self, signal_id: str) -> Dict[str, Any]:
        r = self._s.delete(f"{self.base_url}/signals/{signal_id}")
        r.raise_for_status()
        return r.json()

    def bulk_delete_cards(self, ids: list[str]) -> Dict[str, Any]:
        r = self._s.post(f"{self.base_url}/kb/cards/delete", json={"ids": ids})
        r.raise_for_status()
        return r.json()
