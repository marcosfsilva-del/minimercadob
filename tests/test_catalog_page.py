from app.core import create_app


def test_catalog_page_renders():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "Catálogo".encode() in response.data


def test_cart_counter_hidden_when_empty():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"cart-count" not in response.data


def test_cart_counter_sums_quantities():
    app = create_app()
    client = app.test_client()

    with client.session_transaction() as session:
        session["cart"] = {"1": 3, "2": 2, "4": 4}

    response = client.get("/")

    assert response.status_code == 200
    assert b"cart-count" in response.data
    assert b"badge.textContent = '9';" in response.data
