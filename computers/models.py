from sqlalchemy import Column, Integer, String, Text
from database import Base


class Computer(Base):
    __tablename__ = "computers"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    price = Column(Integer)
    description = Column(Text, nullable=True)    