from prometheus_client import Counter, Histogram, Gauge, Info

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
    ['service', 'method', 'status_code']
)

EXTERNAL_REQUEST_LATENCY = Histogram(
    'external_request_duration_seconds',
    'External service request latency in seconds',
    ['service', 'method']
)

# Application info
APP_INFO = Info('api_info', 'Application information')
