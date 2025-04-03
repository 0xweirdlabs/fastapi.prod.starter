from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.backend.api.deps import get_current_active_superuser, get_current_user, get_db
from src.backend.models.primary.user import User
from src.backend.repositories.user_repository import UserRepository
from src.backend.services.user_service import UserService
from src.backend.api.v1.schemas.user import User as UserSchema
from src.backend.api.v1.schemas.user import UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    user_repo = UserRepository()
    return user_repo.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    db: Session = Depends(get_db),
    user_in: UserCreate = Depends(UserCreate),
    current_user: User = Depends(get_current_active_superuser),
) -> UserSchema:
    """
    Create new user.
    """
    user_repo = UserRepository()
    user_service = UserService(user_repo)
    user = user_service.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    return user_service.create_user(db, user_in)


@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_user),
) -> UserSchema:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserSchema)
def update_user_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user_in: UserUpdate = Depends(UserUpdate),
) -> UserSchema:
    """
    Update own user.
    """
    user_repo = UserRepository()
    user_service = UserService(user_repo)
    return user_service.update_user(db, current_user, user_in)


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> UserSchema:
    """
    Get a specific user by id.
    """
    user_repo = UserRepository()
    user = user_repo.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate = Depends(UserUpdate),
    current_user: User = Depends(get_current_active_superuser),
) -> UserSchema:
    """
    Update a user.
    """
    user_repo = UserRepository()
    user_service = UserService(user_repo)
    user = user_repo.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    return user_service.update_user(db, user, user_in)


@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> UserSchema:
    """
    Delete a user.
    """
    user_repo = UserRepository()
    user = user_repo.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_repo.delete(db, id=user_id)
    return user
