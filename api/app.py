from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from routers import ref_events, support, actions, signals, kb, audit
import logging
import time
import uuid
from services.health import check_all
from config import settings
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="RainRef API", description="Ref Events, Answers, Actions, Signals", version=settings.app_version)

logging.getLogger().setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

app.add_middleware(GZipMiddleware, compresslevel=5)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.cors_allow_credentials,
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
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    dur = (time.time() - start) * 1000
    logger.info(f"{rid} {request.method} {request.url.path} -> {response.status_code} in {dur:.1f}ms")
    return response

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(status_code=404, content={"error": "not_found", "path": request.url.path})
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

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

@app.get("/info")
def info():
    return {"version": settings.app_version, "git_sha": settings.git_sha}

@app.head("/healthz")
def head_health():
    return {}

@app.get("/system/time")
def system_time():
    import datetime
    return {"server_time": datetime.datetime.utcnow().isoformat() + "Z"}
