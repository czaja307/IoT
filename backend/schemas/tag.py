from pydantic import BaseModel, ConfigDict

from schemas import Product


class TagBase(BaseModel):
    id: int


class TagCreate(TagBase):
    product_id: int


class TagUpdate(TagBase):
    product_id: int


class Tag(TagBase):
    model_config = ConfigDict(from_attributes=True)

    product: Product
