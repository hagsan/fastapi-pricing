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

async def get_prices(db: Session, price_request: PriceRequest) -> PriceResponse:
    product_ids = [product.product_id for product in price_request.products]
    query = select(Price).where(
        Price.product_id.in_(product_ids),
        Price.valid_from <= price_request.request_date,
        Price.valid_to >= price_request.request_date,
        Price.currency == price_request.currency
    )
    if price_request.customer_id:
        query = query.where(or_(Price.customer_id == price_request.customer_id, Price.customer_id.is_(None)))
    else:   
        query = query.where(Price.customer_id.is_(None))
    if price_request.customer_group_id:
        query = query.where(or_(Price.customer_group_id == price_request.customer_group_id, Price.customer_group_id.is_(None)))
    else:
        query = query.where(Price.customer_group_id.is_(None))
   
    result = db.execute(query)

    if not result:
        return None

    # Group by product_id
    prices_by_product = {}
    for price_record in result.scalars():
        pid = price_record.product_id
        prices_by_product.setdefault(pid, []).append(price_record)

    price_outputs = []
    for pid, records in prices_by_product.items():
        # Prioritize by customer_id, then customer_group_id, then fallback
        selected = None
        for r in records:
            if price_request.customer_id and r.customer_id == price_request.customer_id:
                selected = r
                break
        if not selected and price_request.customer_group_id:
            for r in records:
                if r.customer_group_id == price_request.customer_group_id:
                    selected = r
                    break
        if not selected:
            selected = r

        price_output = PriceOutput(
            id=selected.id,
            product_id=selected.product_id,
            amount=selected.amount,
            currency=selected.currency,
            customer_id=selected.customer_id,
            customer_group_id=selected.customer_group_id,
            valid_from=selected.valid_from,
            valid_to=selected.valid_to
        )
        price_outputs.append(price_output)
    
    return PriceResponse(prices=price_outputs)