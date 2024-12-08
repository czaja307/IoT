from typing import Optional

from pydantic import BaseModel, field_validator, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float

    @field_validator("price")
    @classmethod
    def round_price(cls, value: float) -> float:
        return round(value, 2)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # tags: List["Tag"] = []
