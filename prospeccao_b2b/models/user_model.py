"""Consultas e comandos da tabela usuarios."""

from db import execute, fetch_all, fetch_one


class UserModel:
    @staticmethod
    def find_by_id(user_id):
        # 1. Evita consulta desnecessaria quando nao ha usuario na sessao.
        if not user_id:
            return None

        # 2. Busca o usuario pelo ID para carregar permissao e dados basicos.
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
        # 3. Busca por e-mail ignorando diferenca entre maiusculas e minusculas.
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
        # 4. Lista usuarios em ordem alfabetica para a tela administrativa.
        return fetch_all(
            """
            SELECT id, nome, email, perfil, ativo, criado_em
              FROM usuarios
             ORDER BY nome
            """
        )

    @staticmethod
    def create(nome, email, senha_hash, perfil="CONSULTOR"):
        # 5. Cria usuario ativo com senha ja convertida para hash.
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
        # 6. Atualiza dados editaveis pelo administrador.
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
        # 7. Troca apenas o hash da senha durante recuperacao de acesso.
        return execute(
            """
            UPDATE usuarios
               SET senha_hash = %(senha_hash)s
             WHERE id = %(id)s
            RETURNING id
            """,
            {"id": user_id, "senha_hash": senha_hash},
        )
