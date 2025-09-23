import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.schemas.price_schema import PriceRequest, ProductPrice, PriceCreate
from src.services.pricing_service import get_prices, create_price

class DummyDBSession(Session):
    def __init__(self):
        self._added = []
        self._committed = False
        self._refreshed = False
        self._rolled_back = False

    def add(self, obj):
        self._added.append(obj)

    def commit(self):
        self._committed = True

    def refresh(self, obj):
        self._refreshed = True

    def rollback(self):
        self._rolled_back = True

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

    prices = await get_prices(db, price_request)
    #assert len(prices) == 1
    assert prices.prices[0].product_id == "prod1"
    assert prices.prices[0].amount == 10.0

@pytest.mark.asyncio
async def test_create_price_success():
    db = DummyDBSession()
    price_data = PriceCreate(
        product_id="1",
        amount=10.0,
        currency="USD",
        customer_id=None,
        customer_group_id=None,
        valid_from="2024-01-01",
        valid_to="2024-12-31"
    )
    result = await create_price(db, price_data)
    assert result.product_id == price_data.product_id
    assert result.amount == price_data.amount
    assert result.currency == price_data.currency
    assert db._committed
    assert db._refreshed

