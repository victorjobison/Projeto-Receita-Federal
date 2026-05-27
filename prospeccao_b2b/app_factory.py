from flask import Flask, g, session

from config import Config
from controllers.admin_controller import admin_bp
from controllers.auth_controller import auth_bp
from controllers.company_controller import company_bp
from controllers.lead_controller import lead_bp
from models.user_model import UserModel


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.before_request
    def carregar_usuario_logado():
        user_id = session.get("user_id")
        g.user = UserModel.find_by_id(user_id) if user_id else None

    app.register_blueprint(auth_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(lead_bp)
    app.register_blueprint(admin_bp)

    return app
