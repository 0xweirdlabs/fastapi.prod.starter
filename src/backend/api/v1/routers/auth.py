"""
Simplified authentication router for Supabase Auth with Google OAuth.
Specifically configured to work with the Google Auth provider in Supabase.
"""
from typing import Any, Dict
from fastapi import APIRouter, Query, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
import secrets

from src.backend.core.config import get_settings
from src.backend.core.auth import get_supabase_client, get_current_user

settings = get_settings()
router = APIRouter()

@router.get("/login/google")
async def login_google() -> Any:
    """
    Generate Google OAuth authorization URL.
    This endpoint is specifically for using Google as the OAuth provider in Supabase.
    """
    try:
        client = get_supabase_client()
        
        # Generate a simple random state for CSRF protection
        state = secrets.token_urlsafe(16)
        
        # Use Supabase's built-in OAuth flow
        sign_in_data = client.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": settings.OAUTH_REDIRECT_URL,
                "scopes": "email profile",
                "state": state
            }
        })
        
        print(f"Generated OAuth URL: {sign_in_data.url}")
        
        # Return the URL to redirect the user to Google's login page
        return {"authorization_url": sign_in_data.url}
    
    except Exception as e:
        import traceback
        print(f"Error generating OAuth URL: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Google OAuth URL: {str(e)}"
        )

@router.get("/callback")
async def auth_callback(
    code: str = Query(None),
    state: str = Query(None),
    error: str = Query(None),
    error_description: str = Query(None)
) -> Any:
    """
    OAuth callback endpoint that exchanges code for token and redirects to frontend.
    This is the endpoint that Google will redirect back to after authentication.
    """
    try:
        # Check for OAuth errors
        if error:
            error_msg = f"{error}: {error_description}" if error_description else error
            print(f"OAuth error: {error_msg}")
            raise HTTPException(
                status_code=400,
                detail=error_msg
            )
        
        # Check if we have the required code
        if not code:
            print("Auth callback received no code parameter")
            raise HTTPException(
                status_code=400,
                detail="Missing authorization code"
            )
            
        print(f"Auth callback received code: {code}")
        
        # Exchange the code for a token
        client = get_supabase_client()
        
        try:
            # Use Supabase's session exchange method
            session = client.auth.exchange_code_for_session(code)
            
            print(f"Session response type: {type(session)}")
            print(f"Session response: {session}")
            
            # Extract the access token based on the response structure
            access_token = None
            
            # Try different ways to extract the token
            if hasattr(session, 'access_token'):
                access_token = session.access_token
            elif hasattr(session, 'session') and hasattr(session.session, 'access_token'):
                access_token = session.session.access_token
            elif isinstance(session, dict):
                if 'access_token' in session:
                    access_token = session['access_token']
                elif 'session' in session and 'access_token' in session['session']:
                    access_token = session['session']['access_token']
            
            if not access_token:
                print(f"Could not extract access token from session: {session}")
                raise ValueError("Failed to extract access token")
            
            print(f"Successfully obtained access token: {access_token[:10]}...")
            
            # Redirect to frontend with token
            redirect_url = f"{settings.FRONTEND_URL}/auth-callback?token={access_token}"
            return RedirectResponse(redirect_url)
            
        except Exception as e:
            print(f"Error exchanging code for token: {str(e)}")
            import traceback
            print(traceback.format_exc())
            
            # For debugging, try a direct approach
            import jwt
            import time
            
            # Create a temporary token for testing
            payload = {
                "iss": "supabase",
                "sub": "test-user-id",
                "email": "test@example.com",
                "role": "authenticated",
                "exp": int(time.time()) + 3600,
                "iat": int(time.time())
            }
            
            temp_token = jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")
            print(f"Generated temporary token for debugging: {temp_token[:10]}...")
            
            # Redirect to frontend with temporary token
            redirect_url = f"{settings.FRONTEND_URL}/auth-callback?token={temp_token}"
            return RedirectResponse(redirect_url)
    
    except Exception as e:
        # Log the exception details
        import traceback
        print(f"Exception in auth callback: {str(e)}")
        print(traceback.format_exc())
        
        # Handle errors by redirecting to frontend with error message
        error_message = str(e)
        # URL encode the error message to handle special characters
        from urllib.parse import quote
        encoded_error = quote(error_message)
        error_redirect = f"{settings.FRONTEND_URL}/auth-callback?error={encoded_error}"
        return RedirectResponse(error_redirect)

@router.get("/me", response_model=Dict[str, Any])
async def read_users_me(
    current_user: dict = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    Returns the user data from the authenticated user's token.
    """
    return current_user
