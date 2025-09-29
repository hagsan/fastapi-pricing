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

    def execute(self, query):
        # Simulate no duplicate found for create_price
        class Result:
            def scalar_one_or_none(self_inner):
                return None
        return Result()

def get_mock_prices():
    return [
        MagicMock(product_id="prod1", amount=20.0, currency="USD", customer_id="cust1", customer_group_id=None, id=1, valid_from="2024-01-01T00:00:00", valid_to="2024-12-31T00:00:00"),
        MagicMock(product_id="prod1", amount=15.0, currency="USD", customer_id=None, customer_group_id="group1", id=2, valid_from="2024-01-01T00:00:00", valid_to="2024-12-31T00:00:00"),
        MagicMock(product_id="prod1", amount=10.0, currency="USD", customer_id=None, customer_group_id=None, id=3, valid_from="2024-01-01T00:00:00", valid_to="2024-12-31T00:00:00"),
        MagicMock(product_id="prod1", amount=5.0, currency="USD", customer_id="cust2", customer_group_id=None, id=4, valid_from="2024-01-01T00:00:00", valid_to="2024-12-31T00:00:00")
    ]

@pytest.mark.asyncio
async def test_create_price_success():
    db = DummyDBSession()
    price_data = PriceCreate(
        product_id="2",
        amount=10.0,
        currency="USD",
        customer_id="2",
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

@pytest.mark.asyncio
async def test_get_price_prioritizes_customer_id(monkeypatch):
    db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value = get_mock_prices()
    db.execute.return_value = mock_result

    price_request = PriceRequest(
        currency="USD",
        customer_id="cust1",
        customer_group_id="group1",
        request_date="2024-06-01T00:00:00",
        products=[ProductPrice(product_id="prod1")]
    )
    prices = await get_prices(db, price_request)
    assert prices.prices[0].amount == 20.0  # Should select price_customer

@pytest.mark.asyncio
async def test_get_price_prioritizes_customer_group_id(monkeypatch):
    db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value = get_mock_prices()
    db.execute.return_value = mock_result

    price_request = PriceRequest(
        currency="USD",
        customer_id=None,
        customer_group_id="group1",
        request_date="2024-06-01T00:00:00",
        products=[ProductPrice(product_id="prod1")]
    )
    prices = await get_prices(db, price_request)
    assert prices.prices[0].amount == 15.0  # Should select price_group

@pytest.mark.asyncio
async def test_get_price_no_matching_customer_id(monkeypatch):
    db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value = get_mock_prices()
    db.execute.return_value = mock_result

    price_request = PriceRequest(
        currency="USD",
        customer_id="cust5",
        customer_group_id="group5",
        request_date="2024-06-01T00:00:00",
        products=[ProductPrice(product_id="prod1")]
    )
    prices = await get_prices(db, price_request)
    assert prices.prices[0].amount == 10.0  # Should select price_default

@pytest.mark.asyncio
async def test_get_price_fallback_to_default(monkeypatch):
    db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value = get_mock_prices()
    db.execute.return_value = mock_result

    price_request = PriceRequest(
        currency="USD",
        request_date="2024-06-01T00:00:00",
        products=[ProductPrice(product_id="prod1")]
    )
    prices = await get_prices(db, price_request)
    assert prices.prices[0].amount == 10.0  # Should select price_default