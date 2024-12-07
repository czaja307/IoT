from typing import Optional, List

from pydantic import BaseModel

from schemas import Tag


class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    tags: List[Tag] = []

    class Config:
        orm_mode = True
