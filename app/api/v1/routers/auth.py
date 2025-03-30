"""
Authentication router for Supabase Auth with Google OAuth support.
Also includes traditional email/password auth for local development.
"""
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import get_settings
from app.core.security import create_access_token
from app.core.auth import SupabaseAuth, get_current_user
from app.services.user_service import UserService
from app.api.v1.schemas.token import Token

settings = get_settings()
router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    Falls back to local authentication if Supabase is not configured.
    """
    # Try Supabase auth first if configured
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        try:
            auth = SupabaseAuth()
            response = await auth.sign_in_with_password(
                email=form_data.username, password=form_data.password
            )
            return {
                "access_token": response.session.access_token,
                "token_type": "bearer",
            }
        except Exception as e:
            # Log the exception but don't expose it to the client
            print(f"Supabase auth failed: {str(e)}")
            # Fall back to local auth if Supabase auth fails
    
    # Local authentication fallback
    user_service = UserService(db)
    user = user_service.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )
    
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=Dict[str, Any])
async def signup(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Any:
    """
    Sign up with email and password.
    Uses Supabase if configured, otherwise falls back to local user creation.
    """
    # Try Supabase auth if configured
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        try:
            auth = SupabaseAuth()
            response = await auth.sign_up(
                email=form_data.username, password=form_data.password
            )
            return {
                "user": response.user.model_dump() if response.user else None,
                "session": response.session.model_dump() if response.session else None,
            }
        except Exception as e:
            # Log the exception but don't expose it to the client
            print(f"Supabase signup failed: {str(e)}")
            # Fall back to local auth if Supabase auth fails
    
    # Local user creation fallback
    user_service = UserService(db)
    existing_user = user_service.get_by_email(email=form_data.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Create a new user
    from app.api.v1.schemas.user import UserCreate
    user_in = UserCreate(
        email=form_data.username,
        password=form_data.password,
        is_active=True,
    )
    user = user_service.create(obj_in=user_in)
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
        },
        "session": None,  # No session for local auth
    }


@router.get("/login/google")
async def login_google() -> Any:
    """
    Generate Google OAuth authorization URL.
    """
    if not (settings.SUPABASE_URL and settings.SUPABASE_KEY):
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth is not configured",
        )
    
    auth = SupabaseAuth()
    authorization_url = auth.get_authorization_url("google")
    return {"authorization_url": authorization_url}


@router.get("/callback")
async def auth_callback(code: str = Query(...)) -> Any:
    """
    OAuth callback endpoint that exchanges code for token and redirects to frontend.
    """
    if not (settings.SUPABASE_URL and settings.SUPABASE_KEY):
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="OAuth callback is not configured",
        )
    
    try:
        auth = SupabaseAuth()
        session = await auth.exchange_code_for_session(code)
        
        # Redirect to frontend with token
        access_token = session.get("access_token", "")
        redirect_url = f"{settings.FRONTEND_URL}/auth-callback?token={access_token}"
        return RedirectResponse(redirect_url)
    except Exception as e:
        # Handle errors
        error_redirect = f"{settings.FRONTEND_URL}/auth-callback?error={str(e)}"
        return RedirectResponse(error_redirect)


@router.post("/logout")
async def logout(
    response: Response,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Any:
    """
    Logout user and invalidate session.
    """
    # For Supabase auth
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        try:
            # The token should be in the Authorization header
            auth = SupabaseAuth()
            await auth.sign_out(None)  # Token is handled by the client
        except Exception as e:
            print(f"Supabase logout failed: {str(e)}")
    
    # For local auth, we can't really invalidate the token,
    # but we can clear the cookie if used
    response.delete_cookie(key="Authorization")
    
    return {"detail": "Successfully logged out"}


@router.get("/me", response_model=Dict[str, Any])
async def read_users_me(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user
