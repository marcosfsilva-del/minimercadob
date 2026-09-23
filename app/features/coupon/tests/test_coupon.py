from flask import session

from app.core import create_app
from app.core.feature_registry import registry
from app.features.coupon.manifest import coupon_form
from app.features.coupon.service import apply_coupon, find_coupon


def test_find_coupon_returns_none_for_unknown_code():
    assert find_coupon("XPTO") is None


def test_find_coupon_returns_none_for_empty_code():
    assert find_coupon("") is None
    assert find_coupon(None) is None


def test_cart_summary_shows_coupon_field():
    app = create_app()

    with app.test_request_context():
        html = "".join(
            slot.renderer(items=[], total=0.0)
            for slot in registry.slot_renderers("CART_SUMMARY")
        )

    assert 'name="coupon"' in html
    assert 'action="/coupon/apply"' in html


def test_apply_unknown_coupon_shows_friendly_message():
    app = create_app()
    client = app.test_client()

    response = client.post("/coupon/apply", data={"coupon": "XPTO"}, follow_redirects=True)

    assert response.status_code == 200
    assert "Cupom não encontrado".encode() in response.data


def test_find_coupon_recognizes_devops10():
    assert find_coupon("DEVOPS10") == 0.10
    assert find_coupon(" devops10 ") == 0.10


def test_apply_coupon_devops10_gives_ten_percent_discount():
    assert apply_coupon(100.0, "DEVOPS10") == {"discount": 10.0, "total": 90.0}


def test_apply_coupon_invalid_keeps_total():
    assert apply_coupon(100.0, "XPTO") == {"discount": 0.0, "total": 100.0}


def test_apply_devops10_saves_coupon_in_session():
    app = create_app()
    client = app.test_client()

    response = client.post("/coupon/apply", data={"coupon": "devops10"}, follow_redirects=True)

    assert b"Cupom DEVOPS10 aplicado" in response.data
    with client.session_transaction() as flask_session:
        assert flask_session["coupon"] == "DEVOPS10"


def test_apply_unknown_coupon_removes_previous_coupon():
    app = create_app()
    client = app.test_client()
    client.post("/coupon/apply", data={"coupon": "DEVOPS10"})

    client.post("/coupon/apply", data={"coupon": "XPTO"})

    with client.session_transaction() as flask_session:
        assert "coupon" not in flask_session


def test_cart_summary_shows_discount_and_final_total():
    app = create_app()

    with app.test_request_context():
        session["coupon"] = "DEVOPS10"
        html = coupon_form(items=[], total=100.0)

    assert "Desconto (DEVOPS10)" in html
    assert "R$ 10,00" in html
    assert "Total final" in html
    assert "R$ 90,00" in html
