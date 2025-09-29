from typing import Dict, Any, Protocol

class BaseAdapter(Protocol):
    name: str
    def perform(self, payload: Dict[str, Any]) -> str: ...

