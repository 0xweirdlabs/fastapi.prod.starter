"""
Item schemas for the example CRUD operations.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    """Base schema for items with common attributes"""
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    """Schema for creating a new item"""
    pass

class ItemUpdate(ItemBase):
    """Schema for updating an existing item"""
    title: Optional[str] = None

class ItemResponse(ItemBase):
    """Schema for item response with database fields"""
    id: int
    owner_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        """Configure Pydantic to work with SQLAlchemy models"""
        orm_mode = True
