"""Rotas HTTP da feature de confirmacao de remocao.

Fluxo em duas etapas:

  1. GET  /confirmar-remocao/<id>  -> mostra a pergunta "tem certeza?"
  2. POST /confirmar-remocao/<id>  -> so aqui o item sai do carrinho

Separar a pergunta (GET) da acao (POST) e o que garante o criterio
"cancelar mantem o item": quem cancela apenas volta para o carrinho,
sem nunca disparar o POST.
"""

from flask import Blueprint, flash, jsonify, redirect, render_template, session, url_for

from app.core.database import session_scope
from app.core.services.market_service import list_products
from app.features.confirmar_remocao.service import mensagem_remocao, remover_item, status

# Blueprint = agrupador de rotas do Flask.
# Quebrado em varias linhas para respeitar o limite
# de 100 caracteres do projeto (regra E501 do Ruff).
bp = Blueprint(
    "confirmar_remocao",              # nome interno do blueprint (usado em url_for)
    __name__,                         # modulo onde o blueprint vive
    url_prefix="/confirmar-remocao",  # prefixo de todas as rotas da feature
    template_folder="templates",      # onde o Flask procura os HTML da feature
)


def _buscar_produto(product_id: int):
    """Busca um produto pelo id usando o servico do core.

    Devolve None quando o id nao existe, para a rota poder responder 404
    em vez de quebrar.
    """
    with session_scope() as db:
        for produto in list_products(db):
            if produto.id == product_id:
                return produto
    return None


@bp.get("/<int:product_id>")
def confirmar(product_id: int):
    """Etapa 1: exibe a pagina de confirmacao.

    Esta rota NAO altera o carrinho. Ela apenas pergunta. E o que torna o
    cancelamento seguro: o usuario pode simplesmente ir embora.
    """
    produto = _buscar_produto(product_id)
    if produto is None:
        return redirect(url_for("web.cart"))

    return render_template("confirmar-remocao.html", produto=produto)


@bp.post("/<int:product_id>")
def remover(product_id: int):
    """Etapa 2: remove de fato o item do carrinho.

    So e alcancada quando o usuario clica em "Confirmar remocao", porque
    o navegador so envia POST ao submeter aquele formulario.
    """
    produto = _buscar_produto(product_id)
    carrinho = session.setdefault("cart", {})

    # A regra de remocao vem do service, que e testavel isoladamente.
    foi_removido = remover_item(carrinho, product_id)
    session.modified = True  # avisa o Flask que a sessao mudou

    # Mensagem so existe quando algo foi realmente removido.
    if foi_removido and produto is not None:
        flash(mensagem_remocao(produto.name))

    return redirect(url_for("web.cart"))


@bp.get("/api")
def api():
    """Endpoint de diagnostico da feature."""
    return jsonify(status())