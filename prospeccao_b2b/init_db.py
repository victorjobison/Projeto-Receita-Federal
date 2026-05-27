from pathlib import Path

from app_factory import create_app
from db import execute, execute_script, fetch_one
from utils.security import hash_password


def main():
    app = create_app()
    with app.app_context():
        schema = Path("schema.sql").read_text(encoding="utf-8")
        execute_script(schema)

        admin_email = app.config["ADMIN_EMAIL"]
        admin = fetch_one("SELECT id FROM usuarios WHERE email = %(email)s", {"email": admin_email})
        if not admin:
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
            print(f"Admin ja existe: {admin_email}")


if __name__ == "__main__":
    main()
