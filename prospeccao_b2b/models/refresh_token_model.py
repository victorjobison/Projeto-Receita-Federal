from db import execute, fetch_one


class RefreshTokenModel:
    @staticmethod
    def create(user_id, token):
        return execute(
            """
            INSERT INTO refresh_tokens (usuario_id, token, expira_em)
            VALUES (%(usuario_id)s, %(token)s, NOW() + INTERVAL '7 days')
            RETURNING token
            """,
            {"usuario_id": user_id, "token": token},
        )

    @staticmethod
    def find_valid(token):
        return fetch_one(
            """
            SELECT rt.id, rt.usuario_id, u.nome, u.email, u.perfil, u.ativo
              FROM refresh_tokens rt
              JOIN usuarios u ON u.id = rt.usuario_id
             WHERE rt.token = %(token)s
               AND rt.revogado_em IS NULL
               AND rt.expira_em >= NOW()
               AND u.ativo = TRUE
            """,
            {"token": token},
        )

    @staticmethod
    def revoke(token):
        return execute(
            """
            UPDATE refresh_tokens
               SET revogado_em = NOW()
             WHERE token = %(token)s
            RETURNING id
            """,
            {"token": token},
        )
