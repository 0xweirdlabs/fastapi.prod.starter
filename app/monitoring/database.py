import time
from functools import wraps
from app.core.monitoring import DB_QUERY_COUNT, DB_QUERY_LATENCY

def track_db_query(operation, table):
    """Decorator to track database query metrics"""
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
