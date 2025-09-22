import asyncio
from src.database.database import SessionLocal
from src.schemas.price import PriceCreate
import src.services.pricing_service as pricing_service
from datetime import datetime

async def create_prices():
    db = SessionLocal()
    try:
        for i in range(1, 1000000):
            payload = PriceCreate(
                product_id=str(1000 + i),
                amount=100 + i,
                currency="EUR",
                valid_from=datetime(2000, 1, 1),
                valid_to=datetime(2030, 1, 1)
            )

            response = await pricing_service.create_price(db, payload)
            print(f"Price row {i} created successfully for product {response.product_id}")
    except Exception as e:
        print(f"Error creating prices: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(create_prices())