import pytest
from unittest.mock import AsyncMock, MagicMock
from src.schemas.cart_schema import Cart, CartEntry
from src.services.cart_service import calculate_cart_total

@pytest.mark.asyncio
async def test_calculate_cart_total_basic(monkeypatch):
    # Mock get_prices to return fixed prices
    mock_prices = MagicMock()
    mock_prices.prices = [
        MagicMock(product_id="prod1", amount=10.0),
        MagicMock(product_id="prod2", amount=5.0)
    ]
    monkeypatch.setattr("src.services.cart_service.get_prices", AsyncMock(return_value=mock_prices))

    cart = Cart(
        items=[
            CartEntry(product_id="prod1", quantity=2),
            CartEntry(product_id="prod2", quantity=3)
        ],
        currency="USD",
        customer_id="cust1",
        customer_group_id=None,
        request_date="2024-06-01T00:00:00"
    )

    result = await calculate_cart_total(None, cart)
    assert result.total_amount == 2 * 10.0 + 3 * 5.0
    assert result.items[0].total == 20.0
    assert result.items[1].total == 15.0

@pytest.mark.asyncio
async def test_calculate_cart_total_missing_price(monkeypatch):
    mock_prices = MagicMock()
    mock_prices.prices = [
        MagicMock(product_id="prod1", amount=10.0)
    ]
    monkeypatch.setattr("src.services.cart_service.get_prices", AsyncMock(return_value=mock_prices))

    cart = Cart(
        items=[CartEntry(product_id="prod2", quantity=1)],
        currency="USD",
        customer_id="cust1",
        customer_group_id=None,
        request_date="2024-06-01T00:00:00"
    )

    with pytest.raises(ValueError):
        await calculate_cart_total(None, cart)
