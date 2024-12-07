from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from controllers.tag import create_tag, get_tags_by_product
from database import get_db
from schemas.tag import TagCreate

router = APIRouter()


@router.post("/", response_model=TagCreate)
def create_new_tag(tag: TagCreate, db: Session = Depends(get_db)):
    return create_tag(db, tag=tag)


@router.get("/{product_id}", response_model=list[TagCreate])
def read_tags_by_product(product_id: int, db: Session = Depends(get_db)):
    return get_tags_by_product(db, product_id=product_id)
