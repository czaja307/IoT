from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class PurchaseProduct(Base):
    __tablename__ = 'purchase_products'

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey('purchases.id', ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)

    purchase = relationship("Purchase")
    product = relationship("Product")

    __table_args__ = (UniqueConstraint('purchase_id', 'product_id', name='uix_product_purchase'))
