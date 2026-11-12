from app.core import create_app
from app.core.models import Order
from app.features.repeat_order.manifest import repeat_button


def test_pedido_exibe_botao_repetir_compra():
    app = create_app()
    pedido = Order(id=7, total=0.0, items=[])
    with app.test_request_context():
        html = repeat_button(order=pedido)
    assert "Repetir compra" in html
    assert "/repeat-order/7" in html