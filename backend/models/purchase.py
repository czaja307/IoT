import datetime

from sqlalchemy import Column, Integer, DateTime

from database import Base


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
