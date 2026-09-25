from app.core import create_app
from app.core.database import session_scope
from app.core.models import Product
from app.features.frete_gratis.service import (
    FREE_SHIPPING_THRESHOLD,
    build_free_shipping_message,
    get_free_shipping_status,
)


def test_compra_abaixo_do_minimo_mostra_valor_faltante():
    status = get_free_shipping_status(12.00)

    assert status["is_free_shipping"] is False
    assert status["remaining"] == 7.99
    assert build_free_shipping_message(12.00) == "Faltam R$ 7,99 para ganhar frete grátis!"


def test_compra_igual_ao_minimo_ganha_frete_gratis():
    status = get_free_shipping_status(19.99)

    assert status["is_free_shipping"] is True
    assert status["remaining"] == 0.0
    assert build_free_shipping_message(19.99) == "Parabéns! Você ganhou frete grátis!"


def test_compra_acima_do_minimo_ganha_frete_gratis():
    status = get_free_shipping_status(25.00)

    assert status["is_free_shipping"] is True
    assert status["remaining"] == 0.0
    assert build_free_shipping_message(25.00) == "Parabéns! Você ganhou frete grátis!"


def test_compra_com_centavos_calcula_restante_corretamente():
    status = get_free_shipping_status(19.98)

    assert status["is_free_shipping"] is False
    assert status["remaining"] == 0.01
    assert build_free_shipping_message(19.98) == "Faltam R$ 0,01 para ganhar frete grátis!"


def test_valor_minimo_esta_documentado_na_constante():
    assert FREE_SHIPPING_THRESHOLD == 19.99


def test_mensagem_aparece_no_carrinho():
    app = create_app()
    with session_scope() as db:
        product = Product(
            name="Produto de teste",
            description="Produto para testar frete",
            category="Teste",
            price=12.00,
            stock=10,
            promotional=False,
        )
        db.add(product)
        db.flush()
        product_id = product.id

    with app.test_client() as client:
        with client.session_transaction() as session:
            session["cart"] = {str(product_id): 1}

        response = client.get("/cart")

    assert response.status_code == 200
    assert b"Faltam R$ 7,99 para ganhar frete gr\xc3\xa1tis!" in response.data
