from prometheus_client import start_http_server
from src.backend.core.config import get_settings

settings = get_settings()

def start_metrics_server():
    """Start Prometheus metrics server."""
    try:
        start_http_server(settings.METRICS_PORT)
        print(f"Metrics server started on port {settings.METRICS_PORT}")
    except Exception as e:
        print(f"Failed to start metrics server: {e}")
