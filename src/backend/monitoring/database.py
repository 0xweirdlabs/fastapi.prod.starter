import time
from functools import wraps
from prometheus_client import Counter, Histogram
from src.backend.core.monitoring import DB_QUERY_COUNT, DB_QUERY_LATENCY

def track_database_query(operation: str, table: str):
    """Decorator to track database query metrics."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                # Record query duration
                DB_QUERY_LATENCY.labels(
                    operation=operation,
                    table=table
                ).observe(time.time() - start_time)
                
                # Count query
                DB_QUERY_COUNT.labels(
                    operation=operation,
                    table=table
                ).inc()
        return wrapper
    return decorator
