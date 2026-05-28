"""Configuracoes centralizadas da aplicacao."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


# 1. Le variaveis do arquivo .env desta pasta antes de montar a classe Config.
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)


def env_obrigatoria(nome: str) -> str:
    valor = os.getenv(nome)
    if not valor:
        raise RuntimeError(f"Variavel de ambiente obrigatoria nao definida: {nome}")
    return valor


def env_int(nome: str, padrao: int, limite_maximo: Optional[int] = None) -> int:
    valor = os.getenv(nome, str(padrao))
    try:
        numero = int(valor)
    except ValueError:
        numero = padrao

    if limite_maximo is not None:
        return min(numero, limite_maximo)
    return numero


def env_int_obrigatoria(nome: str) -> int:
    valor = env_obrigatoria(nome)
    try:
        return int(valor)
    except ValueError as exc:
        raise RuntimeError(f"Variavel de ambiente precisa ser numerica: {nome}") from exc


class Config:
    # 2. Usa as variaveis definidas no arquivo .env, com padroes para desenvolvimento.
    SECRET_KEY = os.getenv("FLASK_SECRET", "dev-secret-change-me")

    # 3. Configura a conexao com PostgreSQL.
    DB_CONFIG = {
        "host": env_obrigatoria("DB_HOST"),
        "port": env_int_obrigatoria("DB_PORT"),
        "dbname": env_obrigatoria("DB_NAME"),
        "user": env_obrigatoria("DB_USER"),
        "password": env_obrigatoria("DB_PASSWORD"),
    }

    # 4. Configura integracoes externas e limites de listagem.
    BRASILAPI_URL = os.getenv("BRASILAPI_URL", "https://brasilapi.com.br/api/cnpj/v1")
    PAGE_SIZE = env_int("PAGE_SIZE", 50, limite_maximo=50)

    # 5. Configura o administrador inicial criado pelo init_db.py.
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@prospeccao.local")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    # 6. Configura assinatura e algoritmo usados nos tokens JWT.
    JWT_SECRET = os.getenv("JWT_SECRET", SECRET_KEY)
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
