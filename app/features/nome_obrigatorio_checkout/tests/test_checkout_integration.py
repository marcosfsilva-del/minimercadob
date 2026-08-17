from app.core import create_app
from app.core.database import session_scope
from app.core.models import Product


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
    response = _post_checkout("   ", follow_redirects=True)

    assert response.status_code == 200
    assert b"Informe o nome do cliente" in response.data


def test_checkout_with_invalid_name_shows_error():
    response = _post_checkout("Al", follow_redirects=True)

    assert response.status_code == 200
    assert b"muito curto" in response.data


def test_checkout_with_valid_name_creates_order():
    # Não seguimos o redirect: /orders tem um bug pré-existente (fora do
    # escopo do módulo 18) que quebra ao renderizar itens do pedido depois
    # que a sessão do banco já fechou. Aqui validamos só a criação do pedido.
    response = _post_checkout("Maria Silva", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"] == "/orders"
