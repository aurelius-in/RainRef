from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import ref_events, support, actions, signals, kb, audit
import os
import logging
import time
import uuid
from services.health import check_all

app = FastAPI(title="RainRef API", description="Ref Events, Answers, Actions, Signals", version="0.1.0")

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.access")

@app.middleware("http")
async def request_id_and_log(request: Request, call_next):
    rid = request.headers.get("X-Request-ID") or f"req-{uuid.uuid4().hex[:8]}"
    start = time.time()
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    dur = (time.time() - start) * 1000
    logger.info(f"{rid} {request.method} {request.url.path} -> {response.status_code} in {dur:.1f}ms")
    return response

app.include_router(ref_events.router, prefix="/ref", tags=["ref-events"])
app.include_router(support.router, prefix="/support", tags=["support"])
app.include_router(actions.router, prefix="/action", tags=["action"])
app.include_router(signals.router, prefix="/signals", tags=["signals"])
app.include_router(kb.router, prefix="/kb", tags=["kb"])
app.include_router(audit.router, prefix="/audit", tags=["audit"])

@app.get("/healthz")
def health():
    return {"ok": True}

@app.get("/healthz/details")
async def health_details():
    details = await check_all()
    return {"ok": all(details.values()), **details}
