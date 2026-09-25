import pytest

from app.features.nome_obrigatorio_checkout.service import status, validate_customer_name


def test_status():
    """Scaffold da feature da Issue #43: o módulo nome-obrigatorio-checkout responde."""
    assert status() == {"feature": "nome-obrigatorio-checkout", "status": "ok"}


def test_validate_customer_name_rejects_empty():
    """Issue #43: nome ausente, vazio ou só com espaços é recusado com mensagem de erro."""
    with pytest.raises(ValueError, match="nome do cliente"):
        validate_customer_name(None)
    with pytest.raises(ValueError, match="nome do cliente"):
        validate_customer_name("")
    with pytest.raises(ValueError, match="nome do cliente"):
        validate_customer_name("   ")


def test_validate_customer_name_strips_and_accepts_valid_name():
    """Issue #43: nome preenchido é aceito e volta sem os espaços das pontas."""
    assert validate_customer_name("  Maria Silva  ") == "Maria Silva"
