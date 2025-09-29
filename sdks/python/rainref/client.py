from typing import Any, Dict
import requests

class RainRefClient:
    def __init__(self, base_url: str = "http://localhost:8080") -> None:
        self.base_url = base_url.rstrip('/')

    def health(self) -> Dict[str, Any]:
        r = requests.get(f"{self.base_url}/healthz")
        r.raise_for_status()
        return r.json()

    def list_events(self) -> Dict[str, Any]:
        r = requests.get(f"{self.base_url}/ref/events")
        r.raise_for_status()
        return r.json()

    def list_actions_by_type(self, type: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        r = requests.get(f"{self.base_url}/action/history/by-type", params={"type": type, "page": page, "limit": limit})
        r.raise_for_status()
        return r.json()

    def delete_signal(self, signal_id: str) -> Dict[str, Any]:
        r = requests.delete(f"{self.base_url}/signals/{signal_id}")
        r.raise_for_status()
        return r.json()

    def bulk_delete_cards(self, ids: list[str]) -> Dict[str, Any]:
        r = requests.post(f"{self.base_url}/kb/cards/delete", json={"ids": ids})
        r.raise_for_status()
        return r.json()
