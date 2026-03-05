from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    books = relationship("Book", back_populates="category", cascade="all, delete-orphan")


class Janre(Base):
    __tablename__ = "janres"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    books = relationship("Book", back_populates="janre")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    price = Column(Integer)
    description = Column(Text, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="books")

    janre_id = Column(Integer, ForeignKey("janres.id"), nullable=False)
    janre = relationship("Janre", back_populates="books")

    comments = relationship("Comment", back_populates="book", cascade="all, delete-orphan")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True)
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String(20), index=True, nullable=False)

    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    book = relationship("Book", back_populates="comments")
    user = relationship("Customer", back_populates="comments")