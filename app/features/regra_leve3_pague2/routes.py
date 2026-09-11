from flask import Blueprint, jsonify, render_template

from app.features.regra_leve3_pague2.service import (
    CATEGORIA_PROMOCIONAL,
    LEVAR,
    PAGAR,
    status,
)

bp = Blueprint(
    "regra_leve3_pague2",
    __name__,
    url_prefix="/regra-leve3-pague2",
    template_folder="templates",
)


@bp.get("")
def page():
    return render_template(
        "regra-leve3-pague2.html",
        categoria=CATEGORIA_PROMOCIONAL,
        levar=LEVAR,
        pagar=PAGAR,
    )


@bp.get("/api")
def api():
    return jsonify(
        {
            **status(),
            "regra": f"Leve {LEVAR}, pague {PAGAR}",
            "categoria": CATEGORIA_PROMOCIONAL,
        }
    )
