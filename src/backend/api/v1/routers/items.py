"""
Protected CRUD operations for Items.
All endpoints require authentication with Supabase.
"""
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.backend.db.session import get_db
from src.backend.models.item import Item
from src.backend.core.auth import get_current_user
from src.backend.api.v1.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from src.backend.api.v1.services.item import ItemService

router = APIRouter()

@router.post("/", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Create a new item.
    This endpoint requires authentication.
    """
    # Create item with current user as owner
    db_item = Item(
        title=item.title,
        description=item.description,
        owner_id=current_user["id"]
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[ItemResponse])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Retrieve items for current user.
    This endpoint requires authentication.
    """
    # Only return items owned by the current user
    items = db.query(Item)\
        .filter(Item.owner_id == current_user["id"])\
        .offset(skip).limit(limit).all()
    return items

@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Get a specific item by ID.
    This endpoint requires authentication and ownership of the item.
    """
    # Only return the item if it belongs to the current user
    item = db.query(Item)\
        .filter(Item.id == item_id, Item.owner_id == current_user["id"])\
        .first()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Update an item.
    This endpoint requires authentication and ownership of the item.
    """
    # Only update the item if it belongs to the current user
    db_item = db.query(Item)\
        .filter(Item.id == item_id, Item.owner_id == current_user["id"])\
        .first()
    
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only provided fields
    if item.title is not None:
        db_item.title = item.title
    if item.description is not None:
        db_item.description = item.description
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Delete an item.
    This endpoint requires authentication and ownership of the item.
    """
    # Only delete the item if it belongs to the current user
    db_item = db.query(Item)\
        .filter(Item.id == item_id, Item.owner_id == current_user["id"])\
        .first()
    
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted successfully"}
