from sqlalchemy import Column, Integer, String, Text
from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    price = Column(Integer)
    description = Column(Text, nullable=True)    
    
    
    
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True)
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String(20), index=True, nullable=False)