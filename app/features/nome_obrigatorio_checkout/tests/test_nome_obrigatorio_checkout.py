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


def test_validate_customer_name_rejects_too_short():
    """Issue #45: nome com menos de 3 caracteres (sem contar espaços) mostra erro."""
    with pytest.raises(ValueError, match="muito curto"):
        validate_customer_name("Al")
    with pytest.raises(ValueError, match="muito curto"):
        validate_customer_name("  Al  ")


def test_validate_customer_name_rejects_too_long():
    """Issue #45: nome com mais de 60 caracteres mostra erro."""
    with pytest.raises(ValueError, match="muito longo"):
        validate_customer_name("A" * 61)


def test_validate_customer_name_accepts_names_within_limits():
    """Issue #45: nomes com exatamente 3 e 60 caracteres são válidos e permitem finalizar."""
    assert validate_customer_name("Ana") == "Ana"
    assert validate_customer_name("A" * 60) == "A" * 60
