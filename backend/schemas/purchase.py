from datetime import datetime

from pydantic import BaseModel


class PurchaseBase(BaseModel):
    pass


class PurchaseCreate(PurchaseBase):
    pass


class Purchase(PurchaseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
