from typing import Optional
from sqlalchemy.orm import Session

from app.models.primary.user import User
from app.repositories.base import BaseRepository
from app.api.v1.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
