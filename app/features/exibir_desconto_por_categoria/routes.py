from flask import Blueprint, render_template

from app.features.exibir_desconto_por_categoria.service import cart_summary

bp = Blueprint(
    "exibir_desconto_por_categoria",
    __name__,
    url_prefix="/exibir-desconto-por-categoria",
    template_folder="templates",
)


def render_cart_summary(items=None, total=0.0, **_context) -> str:
    """Renderer do slot CART_SUMMARY: mostra desconto e total final no resumo."""
    summary = cart_summary(items or [], total)
    return render_template("exibir-desconto-por-categoria.html", summary=summary)
