from flask import Flask

from app.core.config import settings
from app.core.database import init_database
from app.core.feature_registry import registry
from app.core.request_id import init_request_id
from app.core.routes.api import api_bp
from app.core.routes.web import web_bp


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.config["SECRET_KEY"] = settings.secret_key

    init_request_id(app)
    init_database()
    registry.discover(include_example=False)

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    registry.register_blueprints(app)

    @app.context_processor
    def feature_context():
        return {
            "feature_menu_items": registry.menu_items(),
            "slot_renderers": registry.slot_renderers,
        }

    @app.template_filter("brl")
    def brl(value: float):
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return app
