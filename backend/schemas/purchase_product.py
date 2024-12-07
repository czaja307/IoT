from pydantic import BaseModel, Field

from pydantic import BaseModel, Field

from schemas import Product, Purchase


class PurchaseProductBase(BaseModel):
    product_id: int
    purchase_id: int
    quantity: int = Field(..., ge=1)


class PurchaseProductCreate(PurchaseProductBase):
    pass


class PurchaseProduct(PurchaseProductBase):
    id: int
    product: Product
    purchase: Purchase

    class Config:
        orm_mode = True
