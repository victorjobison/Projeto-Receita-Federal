"""Funcoes pequenas para abrir conexao e executar SQL no PostgreSQL."""

from flask import current_app
import psycopg
from psycopg.rows import dict_row


def get_conn():
    # 1. Abre a conexao usando os dados carregados no app Flask.
    return psycopg.connect(
        **current_app.config["DB_CONFIG"],
        row_factory=dict_row,
    )


def fetch_one(sql, params=None):
    # 2. Executa um SELECT e devolve apenas a primeira linha encontrada.
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            return cur.fetchone()


def fetch_all(sql, params=None):
    # 3. Executa um SELECT e devolve todas as linhas encontradas.
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            return cur.fetchall()


def execute(sql, params=None):
    # 4. Executa comandos de escrita e confirma a transacao no banco.
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})

            # 5. Se o SQL tiver RETURNING, captura a linha retornada.
            row = cur.fetchone() if cur.description else None
            conn.commit()
            return row


def execute_script(sql):
    # 6. Executa um script SQL completo, usado principalmente na inicializacao.
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
