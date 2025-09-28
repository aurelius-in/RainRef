from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ref_events, support, actions, signals, kb, audit
import os

app = FastAPI(title="RainRef API")

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ref_events.router, prefix="/ref", tags=["ref-events"])
app.include_router(support.router, prefix="/support", tags=["support"])
app.include_router(actions.router, prefix="/action", tags=["action"])
app.include_router(signals.router, prefix="/signals", tags=["signals"])
app.include_router(kb.router, prefix="/kb", tags=["kb"])
app.include_router(audit.router, prefix="/audit", tags=["audit"])

@app.get("/healthz")
def health():
    return {"ok": True}
