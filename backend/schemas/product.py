from typing import Optional

from pydantic import BaseModel, field_validator, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Price must be greater or equal to 0")
        return round(value, 2)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
