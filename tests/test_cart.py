from app.core import create_app


def test_clear_cart_removes_all_items_and_shows_empty_message():
    app = create_app()
    client = app.test_client()

    with client.session_transaction() as session:
        session["cart"] = {"1": 2, "2": 1}

    response = client.post("/cart/clear", follow_redirects=True)

    assert response.status_code == 200
    assert b"Seu carrinho est\xc3\xa1 vazio." in response.data
    assert b"Limpar carrinho" not in response.data

    with client.session_transaction() as session:
        assert session["cart"] == {}