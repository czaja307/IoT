from typing import List, Optional
from schemas.product import ProductCreate, ProductUpdate, ProductCount
from sqlalchemy.orm import Session
from models import Product, Tag
from sqlalchemy import func


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False


def get_products_count(db: Session) -> list[ProductCount]:
    product_counts = (
        db.query(Product.id, Product.name, func.count(Tag.id).label('count'))
        .outerjoin(Tag, Tag.product_id == Product.id)
        .group_by(Product.id)
        .all()
    )

    product_count_list = [
        ProductCount(id=product.id, name=product.name, count=product.count)
        for product in product_counts
    ]

    return product_count_list
