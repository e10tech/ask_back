# app/crud.py
from sqlalchemy.orm import Session

from app import models, schemas


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    user = models.User(name=user_in.name, email=user_in.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()
