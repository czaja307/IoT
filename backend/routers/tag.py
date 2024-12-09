from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from controllers.tag import create_tag, get_tags_by_product, get_tags, get_tag, update_tag, delete_tag
from database import get_db
from schemas.tag import TagCreate, Tag, TagUpdate

router = APIRouter()


@router.get("/", response_model=list[Tag])
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_tags(db, skip=skip, limit=limit)


@router.get("/{tag_id}", response_model=Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    product = get_tag(db, tag_id=tag_id)
    if not product:
        raise HTTPException(status_code=404, detail="Tag not found")
    return product


@router.post("/", response_model=Tag, status_code=201)
def create_new_tag(tag: TagCreate, db: Session = Depends(get_db)):
    return create_tag(db, tag=tag)


@router.put("/{tag_id}", response_model=Tag)
def update_existing_tag(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)):
    updated_tag = update_tag(db, tag_id=tag_id, tag=tag)
    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated_tag


@router.delete("/{tag_id}", status_code=204)
def delete_existing_tag(tag_id: int, db: Session = Depends(get_db)):
    success = delete_tag(db, tag_id=tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")


@router.get("/by-product/{product_id}")
def read_tags_by_product(product_id: int, db: Session = Depends(get_db)):
    return get_tags_by_product(db, product_id=product_id)
