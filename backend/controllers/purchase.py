from typing import List, Optional

from sqlalchemy.orm import Session

from models.purchase import Purchase
from schemas.purchase import PurchaseCreate


def create_purchase(db: Session, purchase: PurchaseCreate) -> Purchase:
    db_purchase = Purchase(**purchase.model_dump())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase


def get_purchase(db: Session, purchase_id: int) -> Optional[Purchase]:
    return db.query(Purchase).filter(Purchase.id == purchase_id).first()


def get_purchases(db: Session, skip: int = 0, limit: int = 10) -> List[Purchase]:
    return db.query(Purchase).offset(skip).limit(limit).all()
