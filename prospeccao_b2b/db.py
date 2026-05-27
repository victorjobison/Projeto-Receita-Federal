from flask import current_app
import psycopg
from psycopg.rows import dict_row


def get_conn():
    return psycopg.connect(
        host=current_app.config["DB_HOST"],
        port=current_app.config["DB_PORT"],
        dbname=current_app.config["DB_NAME"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        row_factory=dict_row,
    )


def fetch_one(sql, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            return cur.fetchone()


def fetch_all(sql, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            return cur.fetchall()


def execute(sql, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            row = cur.fetchone() if cur.description else None
            conn.commit()
            return row


def execute_script(sql):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
