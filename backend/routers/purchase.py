from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from controllers.purchase import create_purchase, get_purchase, get_purchases
from database import get_db
from schemas.purchase import PurchaseCreate

router = APIRouter()


@router.post("/", response_model=PurchaseCreate, status_code=201)
def create_new_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    return create_purchase(db, purchase=purchase)


@router.get("/{purchase_id}", response_model=PurchaseCreate)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase = get_purchase(db, purchase_id=purchase_id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase


@router.get("/", response_model=list[PurchaseCreate])
def read_purchases(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_purchases(db, skip=skip, limit=limit)
