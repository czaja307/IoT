from sqlalchemy import Column, Integer, Text, Float
from sqlalchemy.orm import relationship

from database import Base
import json

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)

    tags = relationship("Tag", back_populates="product")
