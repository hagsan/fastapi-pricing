from src.schemas.cart_schema import CartEntry, Cart
from sqlalchemy.orm import Session
from src.schemas.price_schema import PriceRequest, ProductPrice
from src.services.pricing_service import get_prices

async def calculate_cart_total(db: Session, cart: Cart) -> Cart:
    price_request = PriceRequest(
        currency=cart.currency,
        customer_id=cart.customer_id,
        customer_group_id=cart.customer_group_id,
        request_date=cart.request_date,
        products=[ProductPrice(product_id=item.product_id) for item in cart.items]
    )
    
    # Get all prices at once
    prices_response = await get_prices(db, price_request)
    
    # Create price lookup dictionary (modified to work with list response)
    price_map = {price.product_id: price.amount for price in prices_response.prices}
    
    total = 0.0
    for item in cart.items:
        if item.product_id not in price_map:
            raise ValueError(f"No price found for product {item.product_id}")
        total += price_map[item.product_id] * item.quantity
    
    cart.total_amount = total
    return cart

def validate_cart(cart: Cart):
    if not cart.items:
        raise ValueError("Cart cannot be empty")
    for item in cart.items:
        if item.quantity <= 0:
            raise ValueError("Quantity must be a positive integer")