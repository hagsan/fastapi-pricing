from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.schemas.price import PriceRequest, PriceResponse, PriceCreate
from src.services.pricing_service import get_prices, create_price
from src.database.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/prices", response_model=PriceResponse)
async def pricing(prices_request: PriceRequest, db: Session = Depends(get_db)):
    try:
        prices = await get_prices(db, prices_request)
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/prices", response_model=PriceCreate)
async def add_price(price_request: PriceCreate, db: Session = Depends(get_db)):
    try:
        price = await create_price(db, price_request)
        return price
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))