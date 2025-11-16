# app/api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserRead)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user_in)


@router.get("/{user_id}", response_model=schemas.UserRead | None)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)
