from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class PurchaseProduct(Base):
    __tablename__ = 'purchase_products'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)

    product = relationship("Product")
    tag = relationship("Tag")

    __table_args__ = (UniqueConstraint('product_id', 'tag_id', name='uix_product_tag'))
