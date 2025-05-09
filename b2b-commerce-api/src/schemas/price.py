from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class ProductPrice(BaseModel):
    product_id: str

class PriceRequest(BaseModel):
    currency: str
    customer_id: Optional[str] = None
    customer_group_id: Optional[str] = None
    request_date: datetime
    products: List[ProductPrice]

class PriceInput(BaseModel):
    product_id: str
    quantity: int

class PriceOutput(BaseModel):
    id: int
    product_id: str
    amount: float
    currency: str
    customer_id: Optional[str] = None
    customer_group_id: Optional[str] = None
    valid_from: datetime
    valid_to: datetime
    model_config = ConfigDict(from_attributes=True)

class PriceResponse(BaseModel):
    prices: List[PriceOutput]

class PriceCreate(BaseModel):
    product_id: str
    amount: float
    currency: str
    customer_id: Optional[str] = None
    customer_group_id: Optional[str] = None
    valid_from: datetime
    valid_to: datetime
    model_config = ConfigDict(from_attributes=True)
