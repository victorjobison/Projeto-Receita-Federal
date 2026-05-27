from db import execute, fetch_all, fetch_one
from psycopg.types.json import Jsonb
from utils.formatters import decimal_or_zero, only_numbers


class CompanyModel:
    @staticmethod
    def upsert_from_api(dados):
        cnpj = only_numbers(dados.get("cnpj"))
        cnae_principal = str(dados.get("cnae_fiscal") or "")
        cnaes_secundarios = dados.get("cnaes_secundarios") or []
        socios = dados.get("qsa") or []

        return execute(
            """
            INSERT INTO empresas (
                cnpj, razao_social, nome_fantasia, cnae_principal,
                cnae_descricao, cnaes_secundarios, porte, capital_social,
                situacao, telefone, email, municipio, uf, logradouro,
                numero, bairro, cep, socios_json, dados_json, atualizado_em
            ) VALUES (
                %(cnpj)s, %(razao_social)s, %(nome_fantasia)s, %(cnae_principal)s,
                %(cnae_descricao)s, %(cnaes_secundarios)s, %(porte)s, %(capital_social)s,
                %(situacao)s, %(telefone)s, %(email)s, %(municipio)s, %(uf)s, %(logradouro)s,
                %(numero)s, %(bairro)s, %(cep)s, %(socios_json)s, %(dados_json)s, NOW()
            )
            ON CONFLICT (cnpj) DO UPDATE SET
                razao_social = EXCLUDED.razao_social,
                nome_fantasia = EXCLUDED.nome_fantasia,
                cnae_principal = EXCLUDED.cnae_principal,
                cnae_descricao = EXCLUDED.cnae_descricao,
                cnaes_secundarios = EXCLUDED.cnaes_secundarios,
                porte = EXCLUDED.porte,
                capital_social = EXCLUDED.capital_social,
                situacao = EXCLUDED.situacao,
                telefone = EXCLUDED.telefone,
                email = EXCLUDED.email,
                municipio = EXCLUDED.municipio,
                uf = EXCLUDED.uf,
                logradouro = EXCLUDED.logradouro,
                numero = EXCLUDED.numero,
                bairro = EXCLUDED.bairro,
                cep = EXCLUDED.cep,
                socios_json = EXCLUDED.socios_json,
                dados_json = EXCLUDED.dados_json,
                atualizado_em = NOW()
            RETURNING *
            """,
            {
                "cnpj": cnpj,
                "razao_social": dados.get("razao_social") or dados.get("nome") or "Sem razao social",
                "nome_fantasia": dados.get("nome_fantasia"),
                "cnae_principal": cnae_principal,
                "cnae_descricao": dados.get("cnae_fiscal_descricao"),
                "cnaes_secundarios": Jsonb(cnaes_secundarios),
                "porte": dados.get("porte"),
                "capital_social": decimal_or_zero(dados.get("capital_social")),
                "situacao": dados.get("descricao_situacao_cadastral") or dados.get("situacao_cadastral"),
                "telefone": dados.get("ddd_telefone_1") or dados.get("telefone"),
                "email": dados.get("email"),
                "municipio": dados.get("municipio"),
                "uf": dados.get("uf"),
                "logradouro": dados.get("logradouro"),
                "numero": dados.get("numero"),
                "bairro": dados.get("bairro"),
                "cep": dados.get("cep"),
                "socios_json": Jsonb(socios),
                "dados_json": Jsonb(dados),
            },
        )

    @staticmethod
    def find_by_cnpj(cnpj):
        return fetch_one(
            "SELECT * FROM empresas WHERE cnpj = %(cnpj)s",
            {"cnpj": only_numbers(cnpj)},
        )

    @staticmethod
    def list_filtered(filters, consultor_id=None, page_size=50):
        where = []
        params = {"limit": page_size, "consultor_id": consultor_id}

        situacao = filters.get("situacao") or "ATIVA"
        if situacao != "TODAS":
            where.append("UPPER(COALESCE(e.situacao, '')) LIKE %(situacao)s")
            params["situacao"] = f"%{situacao.upper()}%"

        if filters.get("cnae"):
            where.append(
                """
                (
                    e.cnae_principal ILIKE %(cnae)s OR
                    e.cnae_descricao ILIKE %(cnae)s OR
                    e.cnaes_secundarios::text ILIKE %(cnae)s
                )
                """
            )
            params["cnae"] = f"%{filters['cnae']}%"

        if filters.get("capital_min"):
            where.append("e.capital_social >= %(capital_min)s")
            params["capital_min"] = decimal_or_zero(filters["capital_min"])

        if filters.get("porte"):
            where.append("e.porte ILIKE %(porte)s")
            params["porte"] = f"%{filters['porte']}%"

        if filters.get("uf"):
            where.append("e.uf = %(uf)s")
            params["uf"] = filters["uf"].upper()

        if filters.get("municipio"):
            where.append("e.municipio ILIKE %(municipio)s")
            params["municipio"] = f"%{filters['municipio']}%"

        if filters.get("busca"):
            where.append(
                """
                (
                    e.razao_social ILIKE %(busca)s OR
                    e.nome_fantasia ILIKE %(busca)s OR
                    e.cnpj ILIKE %(busca)s
                )
                """
            )
            params["busca"] = f"%{filters['busca']}%"

        where_sql = " AND ".join(where) if where else "TRUE"
        return fetch_all(
            f"""
            SELECT e.*,
                   l.id AS lead_id,
                   l.status AS lead_status
              FROM empresas e
              LEFT JOIN leads l
                ON l.empresa_id = e.id
               AND l.consultor_id = %(consultor_id)s
             WHERE {where_sql}
             ORDER BY e.capital_social DESC NULLS LAST, e.razao_social
             LIMIT %(limit)s
            """,
            params,
        )
