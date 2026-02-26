from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import SignUpSchema
import auth

auth_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_router.post("/signup")
def signup(user: SignUpSchema, db: Session = Depends(get_db)):
    return auth.signup(db, user)
