from typing import Optional

from pydantic import BaseModel, Field

from schemas import Product, Tag


class PurchaseProductBase(BaseModel):
    product_id: int
    tag_id: int
    quantity: int = Field(..., ge=1)


class PurchaseProductCreate(PurchaseProductBase):
    pass


class PurchaseProduct(PurchaseProductBase):
    id: int
    product: Optional[Product]
    tag: Optional[Tag]

    class Config:
        orm_mode = True
