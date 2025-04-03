from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.metrics import start_metrics_server
from src.backend.monitoring.middleware import PrometheusMiddleware
from src.backend.core.monitoring import APP_INFO
from src.backend.api.v1.router import router as router_v1
from src.backend.core.config import get_settings

# Import models to create tables
from src.backend.models.item import Base
from src.backend.db.session import engine

# Get settings
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)
