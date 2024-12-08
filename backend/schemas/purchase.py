from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas import Product


class ProductQuantityCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)


class ProductQuantity(BaseModel):
    product: Product
    quantity: int = Field(..., ge=1)


class PurchaseCreate(BaseModel):
    products: list[ProductQuantityCreate]


class Purchase(PurchaseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    products: list[ProductQuantity]
    # total_price: float
    created_at: datetime
