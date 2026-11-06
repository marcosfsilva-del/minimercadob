from app.core import create_app
from app.core.database import SessionLocal
from app.core.models import Product


def test_api_rejects_order_above_stock():
    app = create_app()
    client = app.test_client()

    with SessionLocal() as db:
        product = db.get(Product, 1)
        assert product is not None
        initial_stock = product.stock

    response = client.post(
        "/api/orders",
        json={
            "items": [
                {
                    "productId": 1,
                    "quantity": initial_stock + 1, #quantidade é maior que o estoque disponível
                }
            ]
        },
    )

    assert response.status_code == 400
    assert "Estoque insuficiente" in response.get_json()["error"]

    with SessionLocal() as db:
        product = db.get(Product, 1)
        assert product is not None
        assert product.stock == initial_stock