from pydantic import BaseModel

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