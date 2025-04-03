from stamina import retry, circuit_breaker
from stamina.wait import wait_exponential

# Default retry configuration
default_retry = retry(
    attempts=3,
    wait=wait_exponential(multiplier=1, min_wait=1, max_wait=10),
    retry_on=(ConnectionError, TimeoutError)
)

# Default circuit breaker configuration
default_circuit_breaker = circuit_breaker(
    failure_threshold=5,
    recovery_timeout=30,
    exception_types=(ConnectionError, TimeoutError)
)

# Create specific configurations for different resource types
db_resilience = retry(
    attempts=5,
    wait=wait_exponential(multiplier=2, min_wait=1, max_wait=30),
    retry_on=(ConnectionError, TimeoutError)
)

api_resilience = retry(
    attempts=3,
    wait=wait_exponential(multiplier=1, min_wait=1, max_wait=5),
    retry_on=(ConnectionError, TimeoutError)
)
