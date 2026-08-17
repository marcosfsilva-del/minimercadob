import pytest

from app.core.services.market_service import create_order


def test_create_order_rejects_empty_items():
    with pytest.raises(ValueError, match="pelo menos um item"):
        create_order(session=None, items=[])  # type: ignore[arg-type]


def test_create_order_rejects_empty_customer_name():
    items = [{"product_id": 1, "quantity": 1}]
    with pytest.raises(ValueError, match="nome do cliente"):
        create_order(session=None, items=items, customer_name="   ")  # type: ignore[arg-type]
