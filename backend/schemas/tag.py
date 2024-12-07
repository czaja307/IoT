from pydantic import BaseModel


class TagBase(BaseModel):
    product_id: int


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True
