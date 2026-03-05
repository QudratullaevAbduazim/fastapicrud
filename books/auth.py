from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

from models import Customer, Book, Comment, Category, Janre
from schemas import SignUpSchema, LoginSchema, ProfileUpdateSchema, ResetPasswordSchema, CommentCreateSchema
    
    

from fastapi_jwt_auth2 import AuthJWT
from fastapi_jwt_auth2.exceptions import AuthJWTException
from shared import REFRESH_TOKEN_EXPIRATION_TIME, ACCESS_TOKEN_EXPIRATION_TIME


def signup(db: Session, user: SignUpSchema):
    if db.query(Customer).filter(Customer.username == user.username).first():
        raise HTTPException(status_code=400, detail="Bu username allaqachon mavjud")

    if db.query(Customer).filter(Customer.email == user.email).first():
        raise HTTPException(status_code=400, detail="Bu email allaqachon mavjud")

    new_user = Customer(
        name=user.name,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"status": 201, "message": "User muvaffaqiyatli ro'yxatdan o'tdi", "user": new_user.username}


def login_user(db: Session, user: LoginSchema, Authorize: AuthJWT):
    db_user = db.query(Customer).filter(
        or_(Customer.username == user.username_or_email,
            Customer.email == user.username_or_email)
    ).first()

    if not db_user or not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=400, detail="Username yoki parol noto'g'ri")

    access_token = Authorize.create_access_token(subject=db_user.username, expires_time=ACCESS_TOKEN_EXPIRATION_TIME)
    refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=REFRESH_TOKEN_EXPIRATION_TIME)

    return jsonable_encoder({
        "status": 200,
        "message": "Login muvaffaqiyatli",
        "access_token": access_token,
        "refresh_token": refresh_token
    })


def refresh_access_token(db: Session, Authorize: AuthJWT):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        if not db.query(Customer).filter(Customer.username == current_user).first():
            raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

        new_access_token = Authorize.create_access_token(
            subject=current_user,
            expires_time=ACCESS_TOKEN_EXPIRATION_TIME
        )

        return jsonable_encoder({"status": 200, "msg": "Access token yangilandi", "access_token": new_access_token})
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz refresh token: {str(e)}")


def update_profile(db: Session, Authorize: AuthJWT, profile_data: ProfileUpdateSchema):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()

        db_user = db.query(Customer).filter(Customer.username == current_user).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

        if profile_data.username and profile_data.username != db_user.username:
            exists = db.query(Customer).filter(Customer.username == profile_data.username).first()
            if exists:
                raise HTTPException(status_code=400, detail="Bu username allaqachon mavjud")
            db_user.username = profile_data.username

        if profile_data.email and profile_data.email != db_user.email:
            exists = db.query(Customer).filter(Customer.email == profile_data.email).first()
            if exists:
                raise HTTPException(status_code=400, detail="Bu email allaqachon mavjud")
            db_user.email = profile_data.email

        if profile_data.name:
            db_user.name = profile_data.name

        db.commit()
        db.refresh(db_user)

        return jsonable_encoder({
            "status": 200,
            "message": "Profil muvaffaqiyatli yangilandi",
            "data": {"name": db_user.name, "username": db_user.username, "email": db_user.email}
        })
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz token: {str(e)}")


def reset_password(db: Session, Authorize: AuthJWT, password_data: ResetPasswordSchema):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()

        db_user = db.query(Customer).filter(Customer.username == current_user).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

        if not check_password_hash(db_user.password, password_data.old_password):
            raise HTTPException(status_code=400, detail="Eski parol noto'g'ri")

        if password_data.new_password != password_data.confirm_password:
            raise HTTPException(status_code=400, detail="Yangi parollar mos kelmadi")

        db_user.password = generate_password_hash(password_data.new_password)
        db.commit()

        return jsonable_encoder({"status": 200, "message": "Parol muvaffaqiyatli yangilandi"})
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz token: {str(e)}")


def create_comment_for_book(db: Session, Authorize: AuthJWT, book_id: int, comment_data: CommentCreateSchema):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz token: {e.message}")

    current_user = Authorize.get_jwt_subject()

    db_user = db.query(Customer).filter(Customer.username == current_user).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")

    content = (comment_data.content or "").strip()
    if not content:
        raise HTTPException(status_code=422, detail="Comment bo'sh bo'lishi mumkin emas")

    try:
        new_comment = Comment(content=content, book_id=book_id, user_id=db_user.id)
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Bazaga yozishda xatolik")

    return jsonable_encoder({
        "status": 201,
        "message": "Comment muvaffaqiyatli yaratildi",
        "comment": {"id": new_comment.id, "content": new_comment.content, "book_id": new_comment.book_id, "user_id": new_comment.user_id}
    })


def delete_comment(db: Session, Authorize: AuthJWT, comment_id: int):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz token: {e.message}")

    current_user = Authorize.get_jwt_subject()

    db_user = db.query(Customer).filter(Customer.username == current_user).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment topilmadi")

    if db_comment.user_id != db_user.id:
        raise HTTPException(status_code=403, detail="Bu commentni o'chirishga ruxsat yo'q")

    try:
        db.delete(db_comment)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Bazadan o'chirishda xatolik")

    return jsonable_encoder({"status": 200, "message": "Comment muvaffaqiyatli o'chirildi"})

def create_category(db: Session, Authorize: AuthJWT, name: str):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz token: {e.message}")

    if db.query(Category).filter(Category.name == name).first():
        raise HTTPException(status_code=400, detail="Bu category allaqachon mavjud")

    new_category = Category(name=name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return jsonable_encoder({
        "status": 201,
        "message": "Category muvaffaqiyatli yaratildi",
        "category": {"id": new_category.id, "name": new_category.name}
    })
    
def create_janre(db: Session, Authorize: AuthJWT, name: str):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz token: {e.message}")

    if db.query(Janre).filter(Janre.name == name).first():
        raise HTTPException(status_code=400, detail="Bu janre allaqachon mavjud")

    new_janre = Janre(name=name)
    db.add(new_janre)
    db.commit()
    db.refresh(new_janre)

    return jsonable_encoder({
        "status": 201,
        "message": "Janre muvaffaqiyatli yaratildi",
        "janre": {"id": new_janre.id, "name": new_janre.name}
    })
    
def delete_category(db: Session, Authorize: AuthJWT, category_id: int):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz token: {e.message}")

    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category topilmadi")

    try:
        db.delete(db_category)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Bazadan o'chirishda xatolik")

    return jsonable_encoder({"status": 200, "message": "Category muvaffaqiyatli o'chirildi"})

def delete_janre(db: Session, Authorize: AuthJWT, janre_id: int):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz token: {e.message}")

    db_janre = db.query(Janre).filter(Janre.id == janre_id).first()
    if not db_janre:
        raise HTTPException(status_code=404, detail="Janre topilmadi")

    try:
        db.delete(db_janre)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Bazadan o'chirishda xatolik")

    return jsonable_encoder({"status": 200, "message": "Janre muvaffaqiyatli o'chirildi"})

def get_all_categories(db: Session):
    categories = db.query(Category).all()
    return jsonable_encoder({
        "status": 200,
        "categories": [{"id": category.id, "name": category.name} for category in categories]
    })
def get_all_janres(db: Session):
    janres = db.query(Janre).all()
    return jsonable_encoder({
        "status": 200,
        "janres": [{"id": janre.id, "name": janre.name} for janre in janres]
    })
    
def update_category(db: Session, Authorize: AuthJWT, category_id: int, new_name: str):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz token: {e.message}")

    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category topilmadi")

    if db.query(Category).filter(Category.name == new_name).first():
        raise HTTPException(status_code=400, detail="Bu category allaqachon mavjud")

    db_category.name = new_name
    db.commit()
    db.refresh(db_category)

    return jsonable_encoder({
        "status": 200,
        "message": "Category muvaffaqiyatli yangilandi",
        "category": {"id": db_category.id, "name": db_category.name}
    })
    
def update_janre(db: Session, Authorize: AuthJWT, janre_id: int, new_name: str):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=401, detail=f"Yaroqsiz token: {e.message}")

    db_janre = db.query(Janre).filter(Janre.id == janre_id).first()
    if not db_janre:
        raise HTTPException(status_code=404, detail="Janre topilmadi")

    if db.query(Janre).filter(Janre.name == new_name).first():
        raise HTTPException(status_code=400, detail="Bu janre allaqachon mavjud")

    db_janre.name = new_name
    db.commit()
    db.refresh(db_janre)

    return jsonable_encoder({
        "status": 200,
        "message": "Janre muvaffaqiyatli yangilandi",
        "janre": {"id": db_janre.id, "name": db_janre.name}
    })