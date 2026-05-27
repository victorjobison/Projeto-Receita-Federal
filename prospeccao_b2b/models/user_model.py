from db import execute, fetch_all, fetch_one


class UserModel:
    @staticmethod
    def find_by_id(user_id):
        if not user_id:
            return None
        return fetch_one(
            """
            SELECT id, nome, email, senha_hash, perfil, ativo, criado_em
              FROM usuarios
             WHERE id = %(id)s
            """,
            {"id": user_id},
        )

    @staticmethod
    def find_by_email(email):
        return fetch_one(
            """
            SELECT id, nome, email, senha_hash, perfil, ativo, criado_em
              FROM usuarios
             WHERE lower(email) = lower(%(email)s)
            """,
            {"email": email},
        )

    @staticmethod
    def list_consultores():
        return fetch_all(
            """
            SELECT id, nome, email, perfil, ativo, criado_em
              FROM usuarios
             ORDER BY nome
            """
        )

    @staticmethod
    def create(nome, email, senha_hash, perfil="CONSULTOR"):
        return execute(
            """
            INSERT INTO usuarios (nome, email, senha_hash, perfil, ativo)
            VALUES (%(nome)s, %(email)s, %(senha_hash)s, %(perfil)s, TRUE)
            RETURNING id, nome, email, perfil, ativo
            """,
            {
                "nome": nome,
                "email": email,
                "senha_hash": senha_hash,
                "perfil": perfil,
            },
        )

    @staticmethod
    def update(user_id, nome, email, perfil, ativo):
        return execute(
            """
            UPDATE usuarios
               SET nome = %(nome)s,
                   email = %(email)s,
                   perfil = %(perfil)s,
                   ativo = %(ativo)s
             WHERE id = %(id)s
            RETURNING id, nome, email, perfil, ativo
            """,
            {
                "id": user_id,
                "nome": nome,
                "email": email,
                "perfil": perfil,
                "ativo": ativo,
            },
        )

    @staticmethod
    def update_password(user_id, senha_hash):
        return execute(
            """
            UPDATE usuarios
               SET senha_hash = %(senha_hash)s
             WHERE id = %(id)s
            RETURNING id
            """,
            {"id": user_id, "senha_hash": senha_hash},
        )
