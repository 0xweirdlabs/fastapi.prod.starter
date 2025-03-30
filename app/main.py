from fastapi import FastAPI
from app.metrics import start_metrics_server
from app.monitoring.middleware import PrometheusMiddleware
from app.core.monitoring import APP_INFO
from app.api.v1.router import router as router_v1

app = FastAPI(
    title="FastAPI Backend",
    description="Production-grade FastAPI backend with standardized structure",
    version="0.1.0"
)

# Add Prometheus middleware
app.add_middleware(PrometheusMiddleware)

# Set application info for Prometheus
APP_INFO.info({
    "version": "1.0.0",
    "environment": "production"
})

# Include API routers
app.include_router(router_v1, prefix="/api/v1")

# Start metrics server on separate port
@app.on_event("startup")
def startup_event():
    start_metrics_server()
