from app.core.models import Order, generate_public_code


def test_geracao_codigo_publico_pedido():
    # Testa a função de geração de código isoladamente
    codigo1 = generate_public_code()
    codigo2 = generate_public_code()
    
    # Verifica o formato
    assert len(codigo1) == 8
    assert "-" in codigo1
    
    # Verifica a aleatoriedade
    assert codigo1 != codigo2

def test_pedido_aceita_codigo_publico_diferente_do_id():
    # Cria uma instância de Pedido em memória (sem precisar da fixture do banco)
    pedido = Order(id=500, total=150.0)
    
    # Simula a geração automática que o SQLAlchemy faria no banco
    pedido.public_code = generate_public_code()
    
    # Prova os critérios de aceitação da Issue
    assert pedido.public_code is not None
    assert str(pedido.id) != pedido.public_code