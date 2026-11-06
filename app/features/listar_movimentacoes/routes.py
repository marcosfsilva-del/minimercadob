from flask import Blueprint, jsonify, render_template

from app.features.listar_movimentacoes.service import status

bp = Blueprint(
    "listar_movimentacoes", 
<<<<<<< HEAD
    __name__,
     url_prefix="/listar-movimentacoes",
      template_folder="templates",
=======
    __name__, 
    url_prefix="/listar-movimentacoes", 
    template_folder="templates"
>>>>>>> 7e23d3388912cd1332db14a07767aca3a93e8945
)


@bp.get("")
def page():
    return render_template("listar-movimentacoes.html")


@bp.get("/api")
def api():
    return jsonify(status())
