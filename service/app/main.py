"""Small production-like FastAPI service used as Incident Commander's target repo."""
import logging
import os
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("orders-service")
app = FastAPI(title="Incident Commander Demo Service", version="1.0.0")
ORDERS = [{"id": "ord-100", "user_id": "user-1", "total": 42.50}]

@app.get("/health")
def health(): return {"status": "ok"}

@app.get("/api/users/me")
def current_user():
    profile = None  # intentional incident fixture: null dereference
    return {"id": profile["id"], "name": "Demo User"}

@app.get("/api/orders")
def orders():
    return {"items": ORDERS, "count": len(ORDERS)}

@app.on_event("startup")
def validate_config():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    if not redis_url.startswith("redis://"):
        log.error("StartupConfigError: Invalid REDIS_URL: expected redis:// URL")
        raise RuntimeError("Invalid REDIS_URL")
