from typing import List

from sqlalchemy.orm import Session

from models.purchase_product import PurchaseProduct
from schemas.purchase_product import PurchaseProductCreate


def create_purchase_product(db: Session, purchase_product: PurchaseProductCreate) -> PurchaseProduct:
    db_purchase_product = PurchaseProduct(**purchase_product.model_dump())
    db.add(db_purchase_product)
    db.commit()
    db.refresh(db_purchase_product)
    return db_purchase_product


def get_purchase_products_by_purchase(db: Session, purchase_id: int) -> List[PurchaseProduct]:
    return db.query(PurchaseProduct).filter(PurchaseProduct.purchase_id == purchase_id).all()


def delete_purchase_product(db: Session, purchase_product_id: int) -> bool:
    db_purchase_product = db.query(PurchaseProduct).filter(PurchaseProduct.id == purchase_product_id).first()
    if db_purchase_product:
        db.delete(db_purchase_product)
        db.commit()
        return True
    return False
