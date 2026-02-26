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
        
    
    