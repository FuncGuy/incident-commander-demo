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
    profile = {"id": "user-1", "name": "Demo User"}
    return {"id": profile["id"], "name": profile["name"]}

@app.get("/api/orders")
def orders():
    return {"items": ORDERS, "count": len(ORDERS)}

@app.get("/api/reports/export")
def export_report():
    """Safe OOM simulation: logs the production signature without allocating memory."""
    log.critical("OutOfMemoryError: report export exceeded memory budget")
    raise HTTPException(status_code=503, detail="report export temporarily unavailable")

@app.get("/api/orders/search")
def search_orders():
    """Safe database timeout simulation."""
    log.error("DatabaseTimeout: orders search query exceeded 5s timeout")
    raise HTTPException(status_code=504, detail="database query timeout")

@app.get("/api/payments/charge")
def charge_payment():
    """Dependency outage simulation."""
    log.error("PaymentProviderUnavailable: upstream returned 503")
    raise HTTPException(status_code=503, detail="payment provider unavailable")

@app.get("/api/config/validate")
def validate_runtime_config():
    """Configuration failure simulation."""
    log.error("StartupConfigError: invalid FEATURE_GATE value")
    raise HTTPException(status_code=500, detail="invalid runtime configuration")

@app.on_event("startup")
def validate_config():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    if not redis_url.startswith("redis://"):
        log.error("StartupConfigError: Invalid REDIS_URL: expected redis:// URL")
        raise RuntimeError("Invalid REDIS_URL")
