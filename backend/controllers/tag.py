from typing import List

from sqlalchemy.orm import Session

from models.tag import Tag
from schemas.tag import TagCreate


def create_tag(db: Session, tag: TagCreate) -> Tag:
    db_tag = Tag(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tags_by_product(db: Session, product_id: int) -> List[Tag]:
    return db.query(Tag).filter(Tag.product_id == product_id).all()
