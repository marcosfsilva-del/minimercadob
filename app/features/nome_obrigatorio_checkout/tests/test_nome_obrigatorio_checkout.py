import pytest

from app.features.nome_obrigatorio_checkout.service import status, validate_customer_name


def test_status():
    assert status() == {"feature": "nome-obrigatorio-checkout", "status": "ok"}


def test_validate_customer_name_rejects_empty():
    with pytest.raises(ValueError, match="nome do cliente"):
        validate_customer_name(None)
    with pytest.raises(ValueError, match="nome do cliente"):
        validate_customer_name("   ")


def test_validate_customer_name_strips_and_accepts_valid_name():
    assert validate_customer_name("  Maria Silva  ") == "Maria Silva"
