from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from src.backend.core.security import get_password_hash, verify_password
from src.backend.models.primary.user import User
from src.backend.repositories.user_repository import UserRepository
from src.backend.api.v1.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(User, db)
    
    def get(self, id: int) -> Optional[User]:
        return self.repository.get(id)
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.repository.get_by_email(email=email)
    
    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.repository.get_multi(skip=skip, limit=limit)
    
    def create(self, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
        )
        return self.repository.create(obj_in=db_obj)
    
    def update(
        self, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return self.repository.update(db_obj=db_obj, obj_in=update_data)
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        return user.is_active
    
    def is_superuser(self, user: User) -> bool:
        return user.is_superuser
