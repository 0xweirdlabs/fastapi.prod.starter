import httpx
from src.backend.core.resilience import api_resilience, default_circuit_breaker
from src.backend.monitoring.external import track_external_request

class ResilientApiClient:
    """Base client for external APIs with built-in resilience"""
    
    def __init__(self, base_url: str, service_name: str, timeout: float = 10.0):
        self.base_url = base_url
        self.service_name = service_name
        self.timeout = timeout
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)
    
    @api_resilience
    @default_circuit_breaker
    @track_external_request(service="dynamic", method="get")
    async def get(self, path: str, params: dict = None):
        response = await self.client.get(path, params=params)
        response.raise_for_status()
        return response.json()
    
    @api_resilience
    @default_circuit_breaker
    @track_external_request(service="dynamic", method="post")
    async def post(self, path: str, json: dict = None):
        response = await self.client.post(path, json=json)
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        await self.client.aclose()
