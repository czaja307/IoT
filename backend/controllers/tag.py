from typing import List, Optional

from sqlalchemy.orm import Session

from models.tag import Tag as TagModel
from schemas.tag import TagCreate, TagUpdate, Tag


def get_tag(db: Session, tag_id: int) -> TagModel:
    return db.query(TagModel).filter(TagModel.id == tag_id).first()


def get_tags(db: Session, skip: int = 0, limit: int = 10) -> List[TagModel]:
    return db.query(TagModel).offset(skip).limit(limit).all()


def create_tag(db: Session, tag: TagCreate) -> TagModel:
    db_tag = TagModel(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update_tag(db: Session, tag_id: int, tag: TagUpdate) -> Optional[Tag]:
    db_tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if db_tag:
        for key, value in tag.model_dump(exclude_unset=True).items():
            setattr(db_tag, key, value)
        db.commit()
        db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int):
    db_tag = db.query(TagModel).filter(TagModel.id == tag_id).first()
    if db_tag:
        db.delete(db_tag)
        db.commit()
        db.refresh(db_tag)
        return True


def get_tags_by_product(db: Session, product_id: int) -> List[int]:
    return [tag_id for (tag_id,) in db.query(TagModel.id).filter(TagModel.product_id == product_id).all()]
