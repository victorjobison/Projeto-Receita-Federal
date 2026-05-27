"""Persistencia do historico de interacoes com leads."""

from db import execute, fetch_all, fetch_one


# Tipos validos aceitos no formulario e no CHECK do banco.
TIPOS_INTERACAO = ["LIGACAO", "EMAIL", "REUNIAO", "OUTRO"]


class InteractionModel:
    @staticmethod
    def list_by_lead(lead_id):
        # 1. Lista contatos do lead do mais recente para o mais antigo.
        return fetch_all(
            """
            SELECT i.*, u.nome AS consultor_nome
              FROM interacoes i
              JOIN usuarios u ON u.id = i.consultor_id
             WHERE i.lead_id = %(lead_id)s
             ORDER BY i.data_interacao DESC
            """,
            {"lead_id": lead_id},
        )

    @staticmethod
    def create(lead_id, consultor_id, tipo, descricao):
        # 2. Registra uma nova interacao vinculada ao lead e ao consultor.
        return execute(
            """
            INSERT INTO interacoes (lead_id, consultor_id, tipo, descricao)
            VALUES (%(lead_id)s, %(consultor_id)s, %(tipo)s, %(descricao)s)
            RETURNING id
            """,
            {
                "lead_id": lead_id,
                "consultor_id": consultor_id,
                "tipo": tipo,
                "descricao": descricao,
            },
        )

    @staticmethod
    def find_by_id(interacao_id):
        # 3. Busca interacao isolada para validacoes de edicao/exclusao.
        return fetch_one(
            "SELECT * FROM interacoes WHERE id = %(id)s",
            {"id": interacao_id},
        )

    @staticmethod
    def update(interacao_id, tipo, descricao):
        # 4. Atualiza apenas se a interacao foi criada nas ultimas 24 horas.
        return execute(
            """
            UPDATE interacoes
               SET tipo = %(tipo)s,
                   descricao = %(descricao)s
             WHERE id = %(id)s
               AND data_interacao >= NOW() - INTERVAL '24 hours'
            RETURNING id
            """,
            {"id": interacao_id, "tipo": tipo, "descricao": descricao},
        )

    @staticmethod
    def delete(interacao_id):
        # 5. Remove a interacao, usado pela rota protegida de administrador.
        return execute(
            "DELETE FROM interacoes WHERE id = %(id)s RETURNING id",
            {"id": interacao_id},
        )
