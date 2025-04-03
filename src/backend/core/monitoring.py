from prometheus_client import Counter, Histogram, Gauge, Info
from prometheus_client import make_asgi_app
from fastapi import Request, Response
from typing import Callable, Any
import time

# API metrics
REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total count of API requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'api_request_duration_seconds',
    'API request latency in seconds',
    ['method', 'endpoint']
)

# Database metrics
DB_QUERY_COUNT = Counter(
    'db_queries_total',
    'Total count of database queries',
    ['operation', 'table']
)

DB_QUERY_LATENCY = Histogram(
    'db_query_duration_seconds',
    'Database query latency in seconds',
    ['operation', 'table']
)

# External service metrics
EXTERNAL_REQUEST_COUNT = Counter(
    'external_requests_total',
    'Total count of external service requests',
    ['service', 'status']
)

EXTERNAL_REQUEST_LATENCY = Histogram(
    'external_request_duration_seconds',
    'External service request latency in seconds',
    ['service', 'status']
)

# Application info
APP_INFO = Info('app_info', 'Application info')


class PrometheusMiddleware:
    """Middleware to track API request metrics."""
    
    def __init__(self, app: Any):
        self.app = app
        
    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        start_time = time.time()
        
        async def send_wrapper(message: dict) -> None:
            if message["type"] == "http.response.start":
                duration = time.time() - start_time
                
                REQUEST_COUNT.labels(
                    method=request.method,
                    endpoint=request.url.path,
                    status_code=message["status"]
                ).inc()
                
                REQUEST_LATENCY.labels(
                    method=request.method,
                    endpoint=request.url.path
                ).observe(duration)
            
            await send(message)

        await self.app(scope, receive, send_wrapper)

# Export Prometheus metrics endpoint
prometheus_app = make_asgi_app()
