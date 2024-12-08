from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Purchase as PurchaseModel, PurchaseProduct as PurchaseProductModel, Product as ProductModel
from schemas import Purchase as PurchaseSchema, PurchaseCreate as PurchaseCreateSchema


def create_purchase(db: Session, purchase_data: PurchaseCreateSchema) -> PurchaseSchema:
    # Ensure at least one product is included
    if not purchase_data.products:
        raise HTTPException(status_code=400, detail="At least one product must be included in the purchase")

    # Validate products and prepare quantities
    product_quantities = {}
    for product_item in purchase_data.products:
        product = db.query(ProductModel).filter(ProductModel.id == product_item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_item.product_id} not found")
        product_quantities[product.id] = product_quantities.get(product.id, 0) + product_item.quantity

    # Create purchase record
    new_purchase = PurchaseModel(created_at=datetime.utcnow())
    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)

    # Create purchase-product associations
    purchase_products = []
    for product_id, quantity in product_quantities.items():
        purchase_product = PurchaseProductModel(
            purchase_id=new_purchase.id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(purchase_product)
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        purchase_products.append({
            "product": product,
            "quantity": quantity
        })

    db.commit()

    # Return purchase as schema
    return PurchaseSchema(
        id=new_purchase.id,
        created_at=new_purchase.created_at,
        products=purchase_products
    )


def get_purchase(db: Session, purchase_id: int) -> Optional[PurchaseSchema]:
    # Fetch the purchase
    purchase = db.query(PurchaseModel).filter(PurchaseModel.id == purchase_id).first()
    if not purchase:
        return None

    # Fetch associated purchase products
    purchase_products = (
        db.query(PurchaseProductModel)
        .filter(PurchaseProductModel.purchase_id == purchase.id)
        .all()
    )

    # Build the products list with full product details
    products = []
    for pp in purchase_products:
        product = db.query(ProductModel).filter(ProductModel.id == pp.product_id).first()
        products.append({
            'product': product,
            'quantity': pp.quantity
        })

    # Construct and return the purchase schema
    return PurchaseSchema(
        id=purchase.id,
        created_at=purchase.created_at,
        products=products
    )


def get_purchases(db: Session, skip: int = 0, limit: int = 10) -> List[PurchaseSchema]:
    purchases = db.query(PurchaseModel).offset(skip).limit(limit).all()

    # Prepare responses
    purchase_responses = []
    for purchase in purchases:
        purchase_products = (
            db.query(PurchaseProductModel)
            .filter(PurchaseProductModel.purchase_id == purchase.id)
            .all()
        )

        # Build the products list with full product details
        products = []
        for pp in purchase_products:
            product = db.query(ProductModel).filter(ProductModel.id == pp.product_id).first()
            products.append({
                'product': product,
                'quantity': pp.quantity
            })

        # Construct purchase response
        purchase_response = PurchaseSchema(
            id=purchase.id,
            created_at=purchase.created_at,
            products=products
        )
        purchase_responses.append(purchase_response)

    return purchase_responses


def delete_purchase(db: Session, purchase_id: int) -> bool:
    purchase = db.query(PurchaseModel).filter(PurchaseModel.id == purchase_id).first()
    if not purchase:
        return False
    db.delete(purchase)
    db.commit()
    return True
