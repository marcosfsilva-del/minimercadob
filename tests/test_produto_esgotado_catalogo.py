from app.core import create_app
from app.core.database import session_scope
from app.core.models import Product


def _criar_produto(nome: str, stock: int) -> int:
    with session_scope() as db:
        product = Product(
            name=nome,
            description="Produto de teste",
            category="Teste",
            price=9.99,
            stock=stock,
            promotional=False,
        )
        db.add(product)
        db.flush()
        return product.id


def _remover_produto(product_id: int) -> None:
    with session_scope() as db:
        product = db.get(Product, product_id)
        if product:
            db.delete(product)


def _card_html(html: str, nome: str) -> str:
    start = html.index(nome)
    end = html.index("</article>", start)
    return html[start:end]


def test_produto_esgotado_mostra_texto_esgotado_e_desabilita_botao():
    app = create_app()
    client = app.test_client()

    product_id = _criar_produto("Produto Teste Esgotado", stock=0)
    try:
        response = client.get("/")
        html = response.data.decode()
        card = _card_html(html, "Produto Teste Esgotado")

        assert response.status_code == 200
        assert "esgotado" in card.lower()
        assert "disabled" in card
    finally:
        _remover_produto(product_id)


def test_produto_com_estoque_nao_mostra_esgotado_e_botao_habilitado():
    app = create_app()
    client = app.test_client()

    product_id = _criar_produto("Produto Teste Com Estoque", stock=5)
    try:
        response = client.get("/")
        html = response.data.decode()
        card = _card_html(html, "Produto Teste Com Estoque")

        assert response.status_code == 200
        assert "esgotado" not in card.lower()
        assert "disabled" not in card
    finally:
        _remover_produto(product_id)


def test_produto_esgotado_continua_visivel_no_catalogo():
    app = create_app()
    client = app.test_client()

    product_id = _criar_produto("Produto Teste Visivel Esgotado", stock=0)
    try:
        response = client.get("/")
        html = response.data.decode()

        assert "Produto Teste Visivel Esgotado" in html
    finally:
        _remover_produto(product_id)
