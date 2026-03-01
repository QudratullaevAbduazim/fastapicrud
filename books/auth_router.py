from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import SignUpSchema, LoginSchema, ProfileUpdateSchema, ResetPasswordSchema
import auth
from fastapi_jwt_auth2 import AuthJWT

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


@auth_router.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth.login_user(db, user, Authorize)


@auth_router.post("/refresh")
def refresh_token(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth.refresh_access_token(db, Authorize)


@auth_router.get("/profile")
def profile(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth.profile(db, Authorize)


@auth_router.put("/profile")
def update_profile(update_data: ProfileUpdateSchema,db: Session = Depends(get_db),Authorize: AuthJWT = Depends()):
    return auth.update_profile(db, Authorize, update_data)


@auth_router.put("/reset-password")
def reset_password(password_data: ResetPasswordSchema,db: Session = Depends(get_db),Authorize: AuthJWT = Depends()):
    return auth.reset_password(db, Authorize, password_data)