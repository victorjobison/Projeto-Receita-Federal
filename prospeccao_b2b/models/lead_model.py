from db import execute, fetch_all, fetch_one


STATUS_LEAD = ["Lead Novo", "Em Contato", "Negociando", "Cliente", "Rejeitado"]


class LeadModel:
    @staticmethod
    def create(empresa_id, consultor_id, observacoes=""):
        return execute(
            """
            INSERT INTO leads (empresa_id, consultor_id, status, observacoes)
            VALUES (%(empresa_id)s, %(consultor_id)s, 'Lead Novo', %(observacoes)s)
            ON CONFLICT (empresa_id, consultor_id) DO UPDATE SET
                observacoes = COALESCE(NULLIF(EXCLUDED.observacoes, ''), leads.observacoes),
                atualizado_em = NOW()
            RETURNING id
            """,
            {
                "empresa_id": empresa_id,
                "consultor_id": consultor_id,
                "observacoes": observacoes,
            },
        )

    @staticmethod
    def find_by_id(lead_id):
        return fetch_one(
            """
            SELECT l.*,
                   e.cnpj, e.razao_social, e.nome_fantasia, e.cnae_principal,
                   e.cnae_descricao, e.porte, e.capital_social, e.situacao,
                   e.telefone, e.email, e.municipio, e.uf, e.logradouro,
                   e.numero, e.bairro, e.cep, e.socios_json,
                   u.nome AS consultor_nome
              FROM leads l
              JOIN empresas e ON e.id = l.empresa_id
              JOIN usuarios u ON u.id = l.consultor_id
             WHERE l.id = %(id)s
            """,
            {"id": lead_id},
        )

    @staticmethod
    def list_filtered(user, filters, page_size=50):
        where = []
        params = {"limit": page_size}

        if user["perfil"] != "ADMIN":
            where.append("l.consultor_id = %(consultor_id)s")
            params["consultor_id"] = user["id"]
        elif filters.get("consultor_id"):
            where.append("l.consultor_id = %(consultor_id)s")
            params["consultor_id"] = filters["consultor_id"]

        if filters.get("status"):
            where.append("l.status = %(status)s")
            params["status"] = filters["status"]

        if filters.get("busca"):
            where.append("(e.razao_social ILIKE %(busca)s OR e.cnpj ILIKE %(busca)s)")
            params["busca"] = f"%{filters['busca']}%"

        where_sql = " AND ".join(where) if where else "TRUE"
        return fetch_all(
            f"""
            SELECT l.id, l.status, l.observacoes, l.criado_em, l.atualizado_em,
                   e.cnpj, e.razao_social, e.nome_fantasia, e.uf, e.municipio,
                   u.nome AS consultor_nome
              FROM leads l
              JOIN empresas e ON e.id = l.empresa_id
              JOIN usuarios u ON u.id = l.consultor_id
             WHERE {where_sql}
             ORDER BY l.atualizado_em DESC NULLS LAST, l.criado_em DESC
             LIMIT %(limit)s
            """,
            params,
        )

    @staticmethod
    def update_status(lead_id, status, observacoes=None):
        return execute(
            """
            UPDATE leads
               SET status = %(status)s,
                   observacoes = COALESCE(%(observacoes)s, observacoes),
                   atualizado_em = NOW()
             WHERE id = %(id)s
            RETURNING id
            """,
            {"id": lead_id, "status": status, "observacoes": observacoes},
        )

    @staticmethod
    def delete(lead_id):
        return execute(
            "DELETE FROM leads WHERE id = %(id)s RETURNING id",
            {"id": lead_id},
        )

    @staticmethod
    def report_by_consultor_status():
        return fetch_all(
            """
            SELECT u.nome AS consultor,
                   l.status,
                   COUNT(l.id) AS total
              FROM usuarios u
              LEFT JOIN leads l ON l.consultor_id = u.id
             WHERE u.perfil = 'CONSULTOR'
             GROUP BY u.nome, l.status
             ORDER BY u.nome, l.status
            """
        )
