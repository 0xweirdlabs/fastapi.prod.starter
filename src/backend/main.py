"""
Main application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.api.v1.router import router as router_v1
from src.backend.monitoring import start_metrics_server
from src.backend.core.config import get_settings
from src.backend.core.monitoring import PrometheusMiddleware, APP_INFO

# Import models to create tables
from src.backend.models.item import Base
from src.backend.db.session import engine

# Get settings
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="FastAPI Backend",
    description="Production-grade FastAPI backend with standardized structure",
    version="1.0.0"
)

# Configure CORS with settings from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus middleware
app.add_middleware(PrometheusMiddleware)

# Set application info for Prometheus
APP_INFO.info({
    "version": "1.0.0",
    "environment": settings.ENVIRONMENT
})

# Include API routers
app.include_router(router_v1, prefix="/api/v1")

# Add health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring"""
    return {"status": "healthy"}

# Start metrics server on separate port
@app.on_event("startup")
def startup_event():
    start_metrics_server()

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Backend"}
