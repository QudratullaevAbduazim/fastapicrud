from pydantic import BaseModel

class ComputerCreate(BaseModel):
    brand: str
    model: str
    price: int
    description: str | None = None


class ComputerResponse(BaseModel):
    id: int
    brand: str
    model: str
    price: int
    description: str | None = None

    class Config:
        from_attributes = True