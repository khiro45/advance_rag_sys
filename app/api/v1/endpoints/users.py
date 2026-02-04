from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import User, UserCreate
# from app.crud.user import crud_user (to be created)

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """Retrieve users."""
    # Logic will go here
    return []

@router.post("/", response_model=User)
def create_user(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    """Create new user."""
    # Logic will go here
    return {}
