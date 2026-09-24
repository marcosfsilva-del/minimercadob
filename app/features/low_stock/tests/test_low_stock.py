from unittest.mock import MagicMock, patch

import pytest

from app.core.app_factory import create_app
from app.features.low_stock.service import (
    LOW_STOCK_THRESHOLD,
    filter_low_stock,
    is_low_stock,
    render_product_card_warning,
)

# --- Fixtures do Pytest ---


@pytest.fixture
def app():
    """Cria a aplicação Flask configurada para o ambiente de testes."""
    app = create_app()
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    """Fornece o cliente de testes HTTP do Flask."""
    return app.test_client()


# --- Testes Unitários de Regra de Negócio ---


def test_low_stock_threshold():
    """Garante que o limite configurado seja exatamente 5 unidades."""
    assert LOW_STOCK_THRESHOLD == 5


@pytest.mark.parametrize(
    ("stock_value", "expected"),
    [
        (0, True),
        (1, True),
        (5, True),
        (6, False),
        (10, False),
    ],
)
def test_is_low_stock_threshold_limits(stock_value: int, expected: bool):
    """Testa os limites de borda da função is_low_stock."""
    product = MagicMock(stock=stock_value)
    assert is_low_stock(product) is expected


def test_is_low_stock_handles_none():
    """Garante resiliência caso o produto ou estoque seja nulo."""
    assert is_low_stock(None) is False
    assert is_low_stock(MagicMock(stock=None)) is False


def test_filter_low_stock():
    """Valida a filtragem de uma lista contendo produtos com diferentes estoques."""
    p_low1 = MagicMock(stock=2)
    p_low2 = MagicMock(stock=5)
    p_normal = MagicMock(stock=6)

    products = [p_low1, p_normal, p_low2]
    filtered = filter_low_stock(products)

    assert len(filtered) == 2
    assert p_low1 in filtered
    assert p_low2 in filtered
    assert p_normal not in filtered


def test_render_product_card_warning():
    """Verifica se o aviso HTML é gerado apenas para estoque baixo."""
    p_low = MagicMock(stock=3)
    p_normal = MagicMock(stock=8)

    assert "Estoque Baixo" in render_product_card_warning(product=p_low)
    assert render_product_card_warning(product=p_normal) == ""


# --- Testes de Integração de Rotas com Pytest e Flask ---


def test_low_stock_page_renders_success(client):
    """Testa se a página HTML /low-stock responde com status 200 e título correto."""
    response = client.get("/low-stock")
    assert response.status_code == 200
    assert b"Produtos com Estoque Baixo" in response.data


def test_low_stock_api_endpoint_returns_json(client):
    """Testa se a rota de API /low-stock/api retorna JSON válido."""
    response = client.get("/low-stock/api")
    assert response.status_code == 200
    assert response.is_json
    assert isinstance(response.get_json(), list)


@patch("app.features.low_stock.routes.list_products")
def test_low_stock_page_empty_state(mock_list_products, client):
    """Testa a exibição da mensagem de estado vazio quando não há produtos com estoque baixo."""
    mock_list_products.return_value = [
        MagicMock(stock=10),
        MagicMock(stock=15),
    ]

    response = client.get("/low-stock")
    assert response.status_code == 200
    assert b"Nenhum produto com estoque baixo" in response.data