from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import or_
from src.database.models import Price
from src.schemas.price_schema import PriceRequest, PriceResponse, PriceCreate, PriceOutput

async def create_price(db: Session, price_create: PriceCreate) -> Dict:
    try:
        db_price = Price(**price_create.model_dump())
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return PriceCreate(
            product_id=db_price.product_id,
            amount=db_price.amount,
            currency=db_price.currency,
            customer_id=db_price.customer_id,
            customer_group_id=db_price.customer_group_id,
            valid_from=db_price.valid_from,
            valid_to=db_price.valid_to
        )
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to create price: {str(e)}")

async def get_price(db: Session, request: PriceRequest):
    product_ids = [product.product_id for product in request.products]
    query = select(Price).where(
        Price.product_id.in_(product_ids),
        Price.valid_from <= request.request_date,
        Price.valid_to >= request.request_date,
        Price.currency == request.currency
    )
    if request.customer_id:
        query = query.where(or_(Price.customer_id == request.customer_id, Price.customer_id.is_(None)))
    else:   
        query = query.where(Price.customer_id.is_(None))
    if request.customer_group_id:
        query = query.where(or_(Price.customer_group_id == request.customer_group_id, Price.customer_group_id.is_(None)))
    else:
        query = query.where(Price.customer_group_id.is_(None))
   
    result = db.execute(query)

    if not result:
        return None
    
    price_outputs = []
    
    for price_record in result.scalars():
        price_output = PriceOutput(
            id=price_record.id,
            product_id=price_record.product_id,
            amount=price_record.amount,
            currency=price_record.currency,
            customer_id=price_record.customer_id,
            customer_group_id=price_record.customer_group_id,
            valid_from=price_record.valid_from,
            valid_to=price_record.valid_to
        )
        price_outputs.append(price_output)

    return price_outputs

async def get_prices(db: Session, price_request: PriceRequest) -> List[PriceResponse]:
    prices = await get_price(db, price_request)
    
    return PriceResponse(prices=prices)