from pydantic import BaseModel, Field
from typing import Optional
class BookCreate(BaseModel):
    title: str
    author: str
    price: int
    description: str | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: int
    description: str | None = None

    class Config:
        from_attributes = True
        
        
class SignUpSchema(BaseModel):
    id: int = Optional
    name: str
    username: str = Field(min_length=5, max_length=20)
    email: str = Field(min_length=9, max_length=20)
    password: str = Field(min_length=5, max_length=20)  
    
    
    class Config:
        orm_mode = True
        
class Settings(BaseModel):
    authjwt_secret_key: str = "parol123"


class LoginSchema(BaseModel):
    username_or_email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=5, max_length=50)
    
    class Config:
        orm_mode = True

class ProfileUpdateSchema(BaseModel):
    username:str = Optional
    email:str = Optional
    name:str =Optional
    
    class Config:
        orm_mode = True
        
        
class ResetPasswordSchema(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
    

    
    
    