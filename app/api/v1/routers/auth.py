"""
Simplified authentication router for Supabase Auth with Google OAuth.
"""
from typing import Any, Dict
from fastapi import APIRouter, Query, HTTPException, status, Depends
from fastapi.responses import RedirectResponse

from app.core.config import get_settings
from app.core.auth import get_supabase_client, get_current_user

settings = get_settings()
router = APIRouter()

@router.get("/login/google")
async def login_google() -> Any:
    """
    Generate Google OAuth authorization URL.
    """
    client = get_supabase_client()
    authorization_url = client.auth.get_url_for_provider(
        "google",
        redirect_to=settings.OAUTH_REDIRECT_URL,
        scopes="email profile"
    )
    return {"authorization_url": authorization_url}

@router.get("/callback")
async def auth_callback(code: str = Query(...)) -> Any:
    """
    OAuth callback endpoint that exchanges code for token and redirects to frontend.
    """
    try:
        client = get_supabase_client()
        session = await client.auth.exchange_code_for_session(code)
        
        # Redirect to frontend with token
        access_token = session.session.access_token
        redirect_url = f"{settings.FRONTEND_URL}/auth-callback?token={access_token}"
        return RedirectResponse(redirect_url)
    except Exception as e:
        # Handle errors
        error_redirect = f"{settings.FRONTEND_URL}/auth-callback?error={str(e)}"
        return RedirectResponse(error_redirect)

@router.get("/me", response_model=Dict[str, Any])
async def read_users_me(
    current_user: dict = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
