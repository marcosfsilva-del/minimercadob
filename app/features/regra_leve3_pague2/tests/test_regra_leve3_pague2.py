from app.features.regra_leve3_pague2.service import status


def test_status():
    assert status() == {"feature": "regra-leve3-pague2", "status": "ok"}
