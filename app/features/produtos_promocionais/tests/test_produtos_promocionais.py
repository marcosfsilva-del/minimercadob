import re

import pytest
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core import create_app, database
from app.core.models import Product


@pytest.fixture
def client(monkeypatch):
    engine = create_engine("sqlite://", poolclass=StaticPool)
    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(
        database, "SessionLocal", sessionmaker(bind=engine, expire_on_commit=False)
    )

    try:
        app = create_app()
        app.config["TESTING"] = True
        with database.session_scope() as db:
            db.add_all([
                Product(
                    name="Café promocional",
                    description="Pacote de café",
                    category="Bebidas",
                    price=12.0,
                    stock=10,
                    promotional=True,
                ),
                Product(
                    name="Arroz comum",
                    description="Pacote de arroz",
                    category="Mercearia",
                    price=20.0,
                    stock=10,
                    promotional=False,
                ),
            ])

        yield app.test_client()
    finally:
        engine.dispose()


def return_to_catalog(client, html):
    link = re.search(r'<a\b[^>]*href="([^"]+)"[^>]*>Ver todos os produtos</a>', html)
    assert link is not None, "A página deve oferecer um link de retorno ao catálogo"
    response = client.get(link.group(1))
    assert response.status_code == 200
    return response.get_data(as_text=True)


def test_promotional_catalog_filters_products(client):
    catalog = client.get("/")
    assert catalog.status_code == 200
    catalog_html = catalog.get_data(as_text=True)
    assert "Café promocional" in catalog_html
    assert "Arroz comum" in catalog_html
    assert "Ver promoções" in catalog_html
    assert 'href="/produtos-promocionais"' in catalog_html

    response = client.get("/produtos-promocionais")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Café promocional" in html
    assert "Arroz comum" not in html
    assert "Exibindo apenas produtos promocionais" in html


def test_return_link_restores_full_catalog(client):
    response = client.get("/produtos-promocionais")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Arroz comum" not in html

    catalog_html = return_to_catalog(client, html)
    assert "Café promocional" in catalog_html
    assert "Arroz comum" in catalog_html
    assert "Ver promoções" in catalog_html
    assert "Exibindo apenas produtos promocionais" not in catalog_html


def test_catalog_without_promotions_shows_message_and_return_link(client):
    with database.session_scope() as db:
        db.execute(update(Product).values(promotional=False))

    response = client.get("/produtos-promocionais")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Nenhum produto em promoção no momento." in html
    assert "Café promocional" not in html
    assert "Arroz comum" not in html
    assert '<article class="card">' not in html

    catalog_html = return_to_catalog(client, html)
    assert "Café promocional" in catalog_html
    assert "Arroz comum" in catalog_html
    assert "Nenhum produto em promoção no momento." not in catalog_html


def test_out_of_stock_promotional_product_remains_visible(client):
    with database.session_scope() as db:
        db.execute(update(Product).where(Product.promotional.is_(True)).values(stock=0))

    response = client.get("/produtos-promocionais")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Café promocional" in html
    assert "Arroz comum" not in html
    assert "Estoque: 0" in html
    assert '<button type="submit" disabled>Adicionar ao carrinho</button>' in html
    assert "Nenhum produto em promoção no momento." not in html
