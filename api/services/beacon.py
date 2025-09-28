import uuid
from typing import Dict, Any

def emit_receipt(action: Dict[str, Any]) -> str:
    return f"r-{uuid.uuid4().hex[:8]}"
