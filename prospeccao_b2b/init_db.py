"""Inicializa o banco e garante a existencia do usuario administrador."""

from pathlib import Path

from app_factory import create_app
from db import execute, execute_script, fetch_one
from utils.security import hash_password


def main():
    # 1. Cria a aplicacao para ter acesso ao contexto e as configuracoes.
    app = create_app()
    with app.app_context():
        # 2. Le o schema SQL local e cria as tabelas/indices no PostgreSQL.
        schema = Path("schema.sql").read_text(encoding="utf-8")
        execute_script(schema)

        # 3. Busca o e-mail configurado para o administrador inicial.
        admin_email = app.config["ADMIN_EMAIL"]
        admin = fetch_one("SELECT id FROM usuarios WHERE email = %(email)s", {"email": admin_email})
        if not admin:
            # 4. Se ainda nao existir admin, cria com senha protegida por hash.
            execute(
                """
                INSERT INTO usuarios (nome, email, senha_hash, perfil, ativo)
                VALUES (%(nome)s, %(email)s, %(senha_hash)s, 'ADMIN', TRUE)
                RETURNING id
                """,
                {
                    "nome": "Administrador",
                    "email": admin_email,
                    "senha_hash": hash_password(app.config["ADMIN_PASSWORD"]),
                },
            )
            print(f"Admin criado: {admin_email}")
        else:
            # 5. Se ja existir, evita criar duplicidade.
            print(f"Admin ja existe: {admin_email}")


if __name__ == "__main__":
    # 6. Permite executar a inicializacao com: python init_db.py
    main()
