from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core import create_app, database
from app.core.models import Product


def test_promotional_catalog_filters_products(monkeypatch):
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

        client = app.test_client()
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
    finally:
        engine.dispose()
