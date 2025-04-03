import uvicorn
from fastapi import FastAPI
from prometheus_client import make_asgi_app

# Create metrics app
metrics_app = FastAPI(title="API Metrics")

# Add prometheus metrics route
metrics_asgi_app = make_asgi_app()
metrics_app.mount("/metrics", metrics_asgi_app)

# Add health check route
@metrics_app.get("/health")
async def health_check():
    return {"status": "healthy"}

def start_metrics_server():
    """Start the metrics server on a separate port"""
    # Run in a separate thread to not block main application
    import threading
    thread = threading.Thread(
        target=uvicorn.run,
        args=(metrics_app,),
        kwargs={
            "host": "0.0.0.0",
            "port": 9090,  # Separate port for metrics
            "log_level": "info"
        },
        daemon=True
    )
    thread.start()
    return thread
