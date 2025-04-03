"""
Main router for API v1 that includes all endpoint modules.
"""
from fastapi import APIRouter
from src.backend.api.v1.routers import auth, items

router = APIRouter()

# Include all module routers
router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(items.router, prefix="/items", tags=["items"])
