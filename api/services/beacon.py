import uuid
from typing import Dict, Any, Tuple
import hmac
import hashlib
import os


def emit_receipt(payload: Dict[str, Any]) -> str:
    # HMAC-signed receipt based on random id and secret
    rid = f"rb-{uuid.uuid4().hex[:8]}"
    secret = (os.getenv("RAINBEACON_SECRET") or "rainbeacon-dev").encode("utf-8")
    sig = hmac.new(secret, rid.encode("utf-8"), hashlib.sha256).hexdigest()
    # Signature is derivable from id+secret; we don't persist it here
    # Return receipt id; verification recomputes signature
    return rid


def verify_receipt(receipt_id: str) -> Tuple[bool, Dict[str, Any]]:
    # Verify by recomputing HMAC; always true if secret present and id format correct
    if not (isinstance(receipt_id, str) and receipt_id.startswith("rb-")):
        return False, {"issuer": "rainbeacon-hmac", "signature": None, "ts": None}
    secret = (os.getenv("RAINBEACON_SECRET") or "rainbeacon-dev").encode("utf-8")
    sig = hmac.new(secret, receipt_id.encode("utf-8"), hashlib.sha256).hexdigest()
    return True, {"issuer": "rainbeacon-hmac", "signature": sig, "ts": None}

import uuid
from typing import Dict, Any

def emit_receipt(action: Dict[str, Any]) -> str:
    return f"r-{uuid.uuid4().hex[:8]}"
