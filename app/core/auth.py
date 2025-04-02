"""
Simplified authentication utilities for Supabase Auth with Google OAuth.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from functools import lru_cache

from app.core.config import get_settings

settings = get_settings()

# HTTP Bearer security scheme for token validation
security = HTTPBearer()

@lru_cache
def get_supabase_client() -> Client:
    """
    Create and cache a Supabase client instance.
    
    Returns:
        Client: Supabase client
    """
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get current authenticated user from Supabase
    
    Args:
        credentials: HTTP Authorization credentials with Bearer token
        
    Returns:
        dict: User data
        
    Raises:
        HTTPException: If the token is invalid or expired
    """
    token = credentials.credentials
    try:
        client = get_supabase_client()
        client.auth.set_session(token)
        user_response = await client.auth.get_user()
        return user_response.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
