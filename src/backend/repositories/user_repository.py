from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from src.backend.models.primary.user import User
from src.backend.repositories.base import BaseRepository
from src.backend.api.v1.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=obj_in.hashed_password,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        obj_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj, obj_data)
