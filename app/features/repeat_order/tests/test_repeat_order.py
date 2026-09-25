from app.core.models import Order, OrderItem, Product
from app.features.repeat_order.service import add_items_to_cart, repeat_order_items, status


def test_status():
    assert status() == {"feature": "repeat-order", "status": "ok"}


def test_repetir_pedido_preserva_itens_e_quantidades():
    # Arrange: um pedido antigo com 2 produtos que ainda tem estoque
    arroz = Product(
        id=1, name="Arroz", description="5kg", category="Mercearia",
        price=25.0, stock=10,
    )
    feijao = Product(
        id=2, name="Feijao", description="1kg", category="Mercearia",
        price=8.0, stock=5,
    )
    pedido = Order(
        id=1,
        total=74.0,
        items=[
            OrderItem(product_id=1, product=arroz, quantity=2,
                      unit_price=25.0, subtotal=50.0),
            OrderItem(product_id=2, product=feijao, quantity=3,
                      unit_price=8.0, subtotal=24.0),
        ],
    )

    # Act: repete o pedido
    resultado = repeat_order_items(pedido)

    # Assert: os mesmos itens voltam com as mesmas quantidades
    assert resultado == [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 3},
    ]


def test_itens_repetidos_entram_no_carrinho():
    # Arrange: carrinho que ja tem 1 arroz
    carrinho = {"1": 1}
    itens = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 3},
    ]

    # Act
    resultado = add_items_to_cart(carrinho, itens)

    # Assert: arroz somou (1 + 2) e feijao entrou com 3
    assert resultado == {"1": 3, "2": 3}