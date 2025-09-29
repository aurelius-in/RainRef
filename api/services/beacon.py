import uuid
from typing import Dict, Any, Tuple
import hmac
import hashlib
import os
import time
from sqlalchemy.orm import Session
from models.entities import BeaconReceipt


def emit_receipt(payload: Dict[str, Any], db: Session | None = None) -> str:
    # HMAC-signed receipt based on timestamp + payload
    ts = int(time.time())
    rid = f"rb-{uuid.uuid4().hex[:8]}"
    secret = (os.getenv("RAINBEACON_SECRET") or "rainbeacon-dev").encode("utf-8")
    base = f"{ts}:{rid}:{hashlib.sha256(str(payload).encode('utf-8')).hexdigest()}"
    sig = hmac.new(secret, base.encode("utf-8"), hashlib.sha256).hexdigest()
    if db is not None:
        db.add(BeaconReceipt(id=rid, signature=sig, timestamp=ts, payload=payload))
    return rid


def verify_receipt(receipt_id: str, db: Session | None = None) -> Tuple[bool, Dict[str, Any]]:
    if not (isinstance(receipt_id, str) and receipt_id.startswith("rb-")):
        return False, {"issuer": "rainbeacon-hmac", "signature": None, "timestamp": None}
    if db is None:
        return False, {"issuer": "rainbeacon-hmac", "signature": None, "timestamp": None}
    rec = db.get(BeaconReceipt, receipt_id)
    if not rec:
        return False, {"issuer": "rainbeacon-hmac", "signature": None, "timestamp": None, "reason": "not found"}
    secret = (os.getenv("RAINBEACON_SECRET") or "rainbeacon-dev").encode("utf-8")
    base = f"{rec.timestamp}:{rec.id}:{hashlib.sha256(str(rec.payload).encode('utf-8')).hexdigest()}"
    expected = hmac.new(secret, base.encode("utf-8"), hashlib.sha256).hexdigest()
    ok = hmac.compare_digest(expected, rec.signature)
    return ok, {"issuer": "rainbeacon-hmac", "signature": rec.signature, "timestamp": rec.timestamp, "signature_match": ok}

import uuid
from typing import Dict, Any

