import uuid
from typing import Dict, Any


def emit_receipt(payload: Dict[str, Any]) -> str:
    # Stubbed RainBeacon receipt: return deterministic-ish id
    return f"rb-{uuid.uuid4().hex[:8]}"

import uuid
from typing import Dict, Any

def emit_receipt(action: Dict[str, Any]) -> str:
    return f"r-{uuid.uuid4().hex[:8]}"
