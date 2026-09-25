from types import SimpleNamespace
from unittest.mock import patch

from app.core import create_app


def produto_teste():
    """Cria um produto fictício para testar a interface do catálogo."""
    return SimpleNamespace(
        id=1,
        name="Produto Teste",
        description="Produto usado nos testes de favorito.",
        price=10.00,
        category="Teste",
        stock=10,
        promotional=False,
    )


def test_marcar_produto_como_favorito():
    """Req 088: produto é adicionado aos favoritos na sessão."""
    app = create_app()
    client = app.test_client()

    response = client.post("/favoritar/1", follow_redirects=True)

    assert response.status_code == 200

    with client.session_transaction() as sess:
        assert "favoritos" in sess
        assert 1 in sess["favoritos"]


def test_produto_favoritado_e_exibido_no_catalogo():
    """Req 088: o catálogo informa que o produto está favoritado."""
    app = create_app()
    client = app.test_client()

    with client.session_transaction() as sess:
        sess["favoritos"] = [1]

    with patch(
        "app.core.routes.web.list_products",
        return_value=[produto_teste()],
    ):
        response = client.get("/")

    assert response.status_code == 200
    assert b"Favoritado" in response.data
    assert b"Desfavoritar" in response.data


def test_desmarcar_produto_remove_dos_favoritos():
    """Req 088: favoritar novamente remove o produto da sessão."""
    app = create_app()
    client = app.test_client()

    with client.session_transaction() as sess:
        sess["favoritos"] = [1]

    response = client.post("/favoritar/1", follow_redirects=True)

    assert response.status_code == 200

    with client.session_transaction() as sess:
        assert 1 not in sess["favoritos"]


def test_catalogo_exibe_acao_favoritar():
    """Req 088: produto não favoritado possui ação para favoritar."""
    app = create_app()
    client = app.test_client()

    with patch(
        "app.core.routes.web.list_products",
        return_value=[produto_teste()],
    ):
        response = client.get("/")

    assert response.status_code == 200
    assert b"Favoritar" in response.data
    assert b"Nao favoritado" not in response.data