"""
Authentication utilities for Supabase Auth with Google OAuth.
"""
from typing import Optional, Dict, Any
import os
from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from gotrue import AuthResponse, UserResponse

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
    supabase_url = settings.SUPABASE_URL
    supabase_key = settings.SUPABASE_KEY
    
    # Check if we have the required configuration
    if not supabase_url or not supabase_key:
        if settings.ENVIRONMENT == "development":
            # For development, we might return a dummy client or None
            # This allows the application to start even without Supabase config
            from unittest.mock import MagicMock
            return MagicMock()
        else:
            raise ValueError("Supabase URL and key must be provided")
    
    return create_client(supabase_url, supabase_key)


class SupabaseAuth:
    """Auth utilities for Supabase with Google OAuth"""
    
    @staticmethod
    def get_authorization_url(provider: str = "google") -> str:
        """
        Get the authorization URL for OAuth provider
        
        Args:
            provider: OAuth provider (default: google)
            
        Returns:
            str: OAuth authorization URL
        """
        client = get_supabase_client()
        return client.auth.get_url_for_provider(
            provider,
            redirect_to=settings.OAUTH_REDIRECT_URL,
            scopes="email profile",
        )
    
    @staticmethod
    async def exchange_code_for_session(code: str) -> Dict[str, Any]:
        """
        Exchange OAuth code for session
        
        Args:
            code: OAuth code from redirect
            
        Returns:
            dict: Session data
        """
        client = get_supabase_client()
        # This is for OAuth code exchange
        session = await client.auth.exchange_code_for_session(code)
        return session.model_dump()
    
    @staticmethod
    async def sign_in_with_password(email: str, password: str) -> AuthResponse:
        """
        Sign in with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            AuthResponse: Auth response with session
        """
        client = get_supabase_client()
        return await client.auth.sign_in_with_password({"email": email, "password": password})
    
    @staticmethod
    async def sign_up(email: str, password: str) -> AuthResponse:
        """
        Sign up with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            AuthResponse: Auth response with user data
        """
        client = get_supabase_client()
        return await client.auth.sign_up({"email": email, "password": password})
    
    @staticmethod
    async def sign_out(token: str) -> None:
        """
        Sign out user
        
        Args:
            token: JWT token
        """
        client = get_supabase_client()
        await client.auth.sign_out(token)
    
    @staticmethod
    async def get_user(token: str) -> UserResponse:
        """
        Get user data from token
        
        Args:
            token: JWT token
            
        Returns:
            UserResponse: User data
        """
        client = get_supabase_client()
        client.auth.set_session(token)
        return await client.auth.get_user()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user
    
    Args:
        credentials: HTTP Authorization credentials with Bearer token
        
    Returns:
        dict: User data
        
    Raises:
        HTTPException: If the token is invalid or expired
    """
    token = credentials.credentials
    try:
        auth = SupabaseAuth()
        user_response = await auth.get_user(token)
        return user_response.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
