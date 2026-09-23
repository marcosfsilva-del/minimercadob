from app.core import create_app
from app.core.feature_registry import registry
from app.features.coupon.service import find_coupon


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
