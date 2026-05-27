"""Monta a aplicacao Flask e registra todas as partes do sistema."""

from flask import Flask, g, session

from config import Config
from controllers.admin_controller import admin_bp
from controllers.auth_controller import auth_bp
from controllers.company_controller import company_bp
from controllers.lead_controller import lead_bp
from models.user_model import UserModel


def create_app() -> Flask:
    # 1. Cria a instancia principal do Flask.
    app = Flask(__name__)

    # 2. Carrega as configuracoes vindas de config.py e do arquivo .env.
    app.config.from_object(Config)

    @app.before_request
    def carregar_usuario_logado():
        # 3. Antes de cada rota, tenta recuperar o usuario salvo na sessao.
        user_id = session.get("user_id")

        # 4. Guarda o usuario em g.user para controllers e templates usarem.
        g.user = UserModel.find_by_id(user_id) if user_id else None

    # 5. Registra os blueprints, que agrupam as rotas por area do sistema.
    app.register_blueprint(auth_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(lead_bp)
    app.register_blueprint(admin_bp)

    # 6. Devolve a aplicacao pronta para rodar ou ser testada.
    return app
