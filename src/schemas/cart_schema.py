from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CartEntry(BaseModel):
    product_id: str
    quantity: int
    total: Optional[float] = None

class Cart(BaseModel):
    items: List[CartEntry]
    currency: str
    customer_id: Optional[str] = None
    customer_group_id: Optional[str] = None
    request_date: datetime
    total_amount: Optional[float] = None