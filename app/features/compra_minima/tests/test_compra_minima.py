from app.features.compra_minima.service import status_checkout


def test_checkout_bloqueado_abaixo_do_minimo():
    resultado = status_checkout(total=30.0, minimo=50.0)
    assert resultado["pode_finalizar"] is False


def test_usuario_ve_quanto_falta():
    resultado = status_checkout(total=30.0, minimo=50.0)
    assert resultado["falta"] == 20.0


def test_compra_acima_do_minimo_pode_finalizar():
    resultado = status_checkout(total=80.0, minimo=50.0)
    assert resultado["pode_finalizar"] is True
    assert resultado["falta"] == 0.0