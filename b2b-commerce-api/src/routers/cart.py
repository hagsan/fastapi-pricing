from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.services.cart_service import calculate_cart_total

router = APIRouter()

class CartEntry(BaseModel):
    product_id: int
    quantity: int

class Cart(BaseModel):
    entries: List[CartEntry]

@router.post("/cart/calculate")
async def calculate_cart(cart: Cart):
    try:
        total_cost = calculate_cart_total(cart.entries)
        return {"total_cost": total_cost}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))