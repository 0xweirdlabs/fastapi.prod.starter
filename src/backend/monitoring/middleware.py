import time
from starlette.middleware.base import BaseHTTPMiddleware
from src.backend.core.monitoring import REQUEST_COUNT, REQUEST_LATENCY

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        # Skip monitoring for the metrics endpoint itself
        if not request.url.path.startswith("/metrics"):
            # Record request duration
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(time.time() - start_time)
            
            # Count request
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=response.status_code
            ).inc()
        
        return response
