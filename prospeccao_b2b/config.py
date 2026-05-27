"""Configuracoes centralizadas da aplicacao."""

import os

from dotenv import load_dotenv


# 1. Le variaveis do arquivo .env antes de montar a classe Config.
load_dotenv()


class Config:
    # 2. Define valores padrao para desenvolvimento quando o .env nao existir.
    SECRET_KEY = os.getenv("FLASK_SECRET", "dev-secret-change-me")

    # 3. Configura a conexao com PostgreSQL.
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "prospeccao_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    # 4. Configura integracoes externas e limites de listagem.
    BRASILAPI_URL = os.getenv("BRASILAPI_URL", "https://brasilapi.com.br/api/cnpj/v1")
    PAGE_SIZE = min(int(os.getenv("PAGE_SIZE", "50")), 50)

    # 5. Configura o administrador inicial criado pelo init_db.py.
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@prospeccao.local")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    # 6. Configura assinatura e algoritmo usados nos tokens JWT.
    JWT_SECRET = os.getenv("JWT_SECRET", SECRET_KEY)
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
