from typing import Optional

from pydantic import BaseModel, UUID4


class ProductCreate(BaseModel):
    name: str
    price: float
    count: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    count: Optional[int] = None

class ProductResponse(BaseModel):
    id: UUID4
    name: str
    price: float
    count: int

    class Config:
        from_attributes = True