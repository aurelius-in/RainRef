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
