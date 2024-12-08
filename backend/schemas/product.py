from typing import Optional, List

from pydantic import BaseModel


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
    tags: List["Tag"] = []

    class Config:
        from_attributes = True
