from pydantic import BaseModel
from typing import List, Optional

class CartItem(BaseModel):
    product_id: str
    quantity: int

class Cart(BaseModel):
    items: List[CartItem]

class CartTotalResponse(BaseModel):
    total_amount: float
    currency: str
    items: List[CartItem]