from app.core import create_app


def test_catalog_page_renders():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "Catálogo".encode() in response.data


def test_catalog_page_has_search_input():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b'name="q"' in response.data
    assert b"Buscar produto" in response.data


def test_catalog_page_filters_products_by_search_term(monkeypatch):
    class ProductStub:
        def __init__(
            self,
            product_id: int,
            name: str,
            description: str,
            category: str,
            price: float,
            stock: int,
            promotional: bool,
        ):
            self.id = product_id
            self.name = name
            self.description = description
            self.category = category
            self.price = price
            self.stock = stock
            self.promotional = promotional

    products = [
        ProductStub(1, "Arroz", "Pacote de arroz branco 5kg", "Mercearia", 24.90, 30, True),
        ProductStub(2, "Sabonete", "Sabonete perfumado 90g", "Higiene", 2.49, 80, True),
    ]

    monkeypatch.setattr("app.core.routes.web.list_products", lambda _db: products)

    app = create_app()
    client = app.test_client()
    response = client.get("/?q=arroz")

    assert response.status_code == 200
    assert b"Arroz" in response.data
    assert b"Sabonete" not in response.data
