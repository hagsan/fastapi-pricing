from fastapi import APIRouter, HTTPException, Depends
from src.schemas.cart_schema import Cart
from src.services.cart_service import calculate_cart_total
from src.database.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/cart/calculate", response_model=Cart)
async def calculate_cart(cart: Cart, db: Session = Depends(get_db)):
    try:
        return await calculate_cart_total(db, cart)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))