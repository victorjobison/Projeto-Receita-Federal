"""Persistencia dos tokens temporarios de recuperacao de senha."""

from db import execute, fetch_one


class PasswordResetModel:
    @staticmethod
    def create(user_id, token):
        # 1. Cria token com validade de 1 hora para o usuario informado.
        return execute(
            """
            INSERT INTO password_reset_tokens (usuario_id, token, expira_em)
            VALUES (%(usuario_id)s, %(token)s, NOW() + INTERVAL '1 hour')
            RETURNING token
            """,
            {"usuario_id": user_id, "token": token},
        )

    @staticmethod
    def find_valid(token):
        # 2. Aceita apenas token existente, nao usado e ainda nao expirado.
        return fetch_one(
            """
            SELECT id, usuario_id, token
              FROM password_reset_tokens
             WHERE token = %(token)s
               AND usado_em IS NULL
               AND expira_em >= NOW()
            """,
            {"token": token},
        )

    @staticmethod
    def mark_used(token_id):
        # 3. Marca token como usado para impedir reutilizacao do link.
        return execute(
            """
            UPDATE password_reset_tokens
               SET usado_em = NOW()
             WHERE id = %(id)s
            RETURNING id
            """,
            {"id": token_id},
        )
