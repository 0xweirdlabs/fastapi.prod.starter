from fastapi import APIRouter
from app.api.v1.routers import users, auth

router = APIRouter()

# Include all module routers
router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(users.router, prefix="/users", tags=["users"])
