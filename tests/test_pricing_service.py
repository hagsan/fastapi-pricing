import pytest
from unittest.mock import MagicMock
from src.schemas.price_schema import PriceRequest, ProductPrice
from src.services.pricing_service import get_price, get_prices

@pytest.mark.asyncio
async def test_get_price_returns_prices(monkeypatch):
    db = MagicMock()
    # Mock db.execute to return a result with scalars
    mock_price_record = MagicMock(
        id=1,
        product_id="prod1",
        amount=10.0,
        currency="USD",
        customer_id="cust1",
        customer_group_id=None,
        valid_from="2024-01-01T00:00:00",
        valid_to="2024-12-31T00:00:00"
    )
    mock_result = MagicMock()
    mock_result.scalars.return_value = [mock_price_record]
    db.execute.return_value = mock_result

    price_request = PriceRequest(
        currency="USD",
        customer_id="cust1",
        customer_group_id=None,
        request_date="2024-06-01T00:00:00",
        products=[ProductPrice(product_id="prod1")]
    )

    prices = await get_price(db, price_request)
    assert len(prices) == 1
    assert prices[0].product_id == "prod1"
    assert prices[0].amount == 10.0

