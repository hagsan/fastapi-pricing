from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from src.database.database import Base

class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False, index=True)
    customer_id = Column(String, index=True)
    customer_group_id = Column(String, index=True)
    valid_from = Column(DateTime, nullable=False, index=True)
    valid_to = Column(DateTime, nullable=False, index=True)

    # Add composite index for common query patterns
    __table_args__ = (
        Index('idx_price_lookup', 'product_id', 'currency', 'customer_id', 'valid_from', 'valid_to'),
    )