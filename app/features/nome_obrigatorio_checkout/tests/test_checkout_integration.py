from sqlalchemy import select

from app.core import create_app
from app.core.database import session_scope
from app.core.models import Order, Product


def _create_test_product() -> int:
    with session_scope() as db:
        product = Product(
            name="Produto Teste Nome Cliente",
            description="produto usado nos testes de validacao de nome",
            category="teste",
            price=10.0,
            stock=5,
        )
        db.add(product)
        db.flush()
        return product.id


def _post_checkout(customer_name: str, follow_redirects: bool = False):
    app = create_app()
    client = app.test_client()
    product_id = _create_test_product()

    with client.session_transaction() as sess:
        sess["cart"] = {str(product_id): 1}

    return client.post(
        "/checkout", data={"customer_name": customer_name}, follow_redirects=follow_redirects
    )


def test_checkout_with_empty_name_shows_error():
    """Issue #47 (regra da #43): nome vazio no checkout mostra erro e não finaliza o pedido."""
    response = _post_checkout("   ", follow_redirects=True)

    assert response.request.path == "/checkout"  # voltou para o checkout
    assert response.status_code == 200
    assert b"Informe o nome do cliente" in response.data


def test_checkout_with_invalid_name_shows_error():
    """Issue #47 (regra da #45): nome inválido por ser curto demais mostra erro no checkout."""
    response = _post_checkout("Al", follow_redirects=True)

    assert response.request.path == "/checkout"
    assert response.status_code == 200
    assert b"muito curto" in response.data


def test_checkout_with_too_long_name_shows_error():
    """Issue #47 (regra da #45): nome inválido por ser longo demais mostra erro no checkout."""
    # O maxlength do HTML pode ser burlado num POST direto; quem garante é o servidor.
    response = _post_checkout("A" * 61, follow_redirects=True)

    assert response.request.path == "/checkout"
    assert response.status_code == 200
    assert b"muito longo" in response.data


def test_checkout_with_valid_name_creates_order():
    """Issue #47 (regras da #43 e #45): nome válido finaliza e o pedido é salvo com ele."""
    # Não seguimos o redirect: /orders tem um bug pré-existente (fora do
    # escopo do módulo 18) que quebra ao renderizar itens do pedido depois
    # que a sessão do banco já fechou. Conferimos o redirect e o banco.
    response = _post_checkout("Maria Silva", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"] == "/orders"
    with session_scope() as db:
        last_order = db.scalars(select(Order).order_by(Order.id.desc())).first()
        assert last_order.customer_name == "Maria Silva"


def test_api_rejects_order_without_customer_name():
    """Issue #47 (regra da #43 na API): pedido sem nome pela API volta 400 com o erro."""
    client = create_app().test_client()
    product_id = _create_test_product()

    response = client.post(
        "/api/orders",
        json={"customerName": "", "items": [{"productId": product_id, "quantity": 1}]},
    )

    assert response.status_code == 400
    assert "nome do cliente" in response.get_json()["error"]
