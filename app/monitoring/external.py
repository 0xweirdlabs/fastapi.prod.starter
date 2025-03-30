import time
from functools import wraps
from app.core.monitoring import EXTERNAL_REQUEST_COUNT, EXTERNAL_REQUEST_LATENCY

def track_external_request(service, method):
    """Decorator to track external service request metrics"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                # Count successful request
                EXTERNAL_REQUEST_COUNT.labels(
                    service=service,
                    method=method,
                    status_code="success"
                ).inc()
                return result
            except Exception as e:
                # Count failed request
                EXTERNAL_REQUEST_COUNT.labels(
                    service=service,
                    method=method,
                    status_code="error"
                ).inc()
                raise e
            finally:
                # Record request duration
                EXTERNAL_REQUEST_LATENCY.labels(
                    service=service,
                    method=method
                ).observe(time.time() - start_time)
        return wrapper
    return decorator
