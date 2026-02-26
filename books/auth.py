from fastapi import HTTPException, status
from models import Customer
from schemas import SignUpSchema
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

def signup(db: Session, user: SignUpSchema):
    db_username = db.query(Customer).filter(Customer.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu username allaqachon mavjud")
    db_email = db.query(Customer).filter(Customer.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu email allaqachon mavjud")
    
    new_user = Customer(
        name=user.name,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    response = {
        'status': status.HTTP_201_CREATED,
        'message': 'User muvaffaqiyatli ro\'yxatdan o\'tdi',
        'user': new_user.username
    }
    return response

