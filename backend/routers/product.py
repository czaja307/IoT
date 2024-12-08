from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from controllers.product import (
    get_product,
    get_products,
    create_product,
    update_product,
    delete_product,
)
from database import get_db
from schemas.product import ProductCreate, ProductUpdate, Product

router = APIRouter()


@router.get("/", response_model=list[Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductCreate, status_code=201)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product=product)


@router.put("/{product_id}", response_model=ProductCreate)
def update_existing_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated_product = update_product(db, product_id=product_id, product=product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{product_id}", status_code=204)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    success = delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
