"""
Módulo Administrativo (RF-20 a RF-23)
Endpoints para cadastro, edição de consultores, relatório global e log de auditoria.
Utiliza FastAPI e integração com PostgreSQL.
"""
from Trabalho_Receita_Federal.Segurança.Dependencias import obter_usuario_atual
from Trabalho_Receita_Federal.Segurança.Segurança import gerar_hash_senha
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
import os

# Configuração de conexão com o banco de dados PostgreSQL
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'receita_federal')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

router = APIRouter()

# Modelos Pydantic para entrada e saída de dados
class ConsultorCreate(BaseModel):
    nome: str
    email: str
    senha: str

class ConsultorUpdate(BaseModel):
    nome: Optional[str]
    email: Optional[str]
    status: Optional[str]  # ativo/inativo

class ConsultorOut(BaseModel):
    id: int
    nome: str
    email: str
    status: str

class RelatorioGlobal(BaseModel):
    consultor: str
    total_leads: int
    leads_por_status: dict

class LogAuditoria(BaseModel):
    id: int
    usuario: str
    acao: str
    data: str

# Função utilitária para conectar ao banco

def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# RF-20: Cadastrar Consultor
@router.post("/admin/consultores", response_model=ConsultorOut)
def cadastrar_consultor(consultor: ConsultorCreate):
    """Cadastra um novo consultor."""
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO consultores (nome, email, senha, status)
            VALUES (%s, %s, %s, 'ativo') RETURNING id, nome, email, status
        """, (consultor.nome, consultor.email, consultor.senha))
        result = cur.fetchone()
        conn.commit()
        return ConsultorOut(id=result[0], nome=result[1], email=result[2], status=result[3])
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# RF-21: Editar Consultor
@router.put("/admin/consultores/{consultor_id}", response_model=ConsultorOut)
def editar_consultor(consultor_id: int, consultor: ConsultorUpdate):
    """Edita dados e status de um consultor."""
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        campos = []
        valores = []
        if consultor.nome:
            campos.append("nome = %s")
            valores.append(consultor.nome)
        if consultor.email:
            campos.append("email = %s")
            valores.append(consultor.email)
        if consultor.status:
            campos.append("status = %s")
            valores.append(consultor.status)
        if not campos:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar.")
        valores.append(consultor_id)
        cur.execute(f"""
            UPDATE consultores SET {', '.join(campos)} WHERE id = %s RETURNING id, nome, email, status
        """, tuple(valores))
        result = cur.fetchone()
        conn.commit()
        if not result:
            raise HTTPException(status_code=404, detail="Consultor não encontrado.")
        return ConsultorOut(id=result[0], nome=result[1], email=result[2], status=result[3])
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# RF-22: Relatório Global
@router.get("/admin/relatorio", response_model=List[RelatorioGlobal])
def relatorio_global():
    """Exibe total de leads por status e por consultor."""
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.nome, COUNT(l.id),
                json_object_agg(l.status, total) as leads_por_status
            FROM consultores c
            LEFT JOIN leads l ON l.consultor_id = c.id
            LEFT JOIN (
                SELECT consultor_id, status, COUNT(*) as total
                FROM leads GROUP BY consultor_id, status
            ) ls ON ls.consultor_id = c.id
            GROUP BY c.nome
        """)
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append(RelatorioGlobal(consultor=row[0], total_leads=row[1], leads_por_status=row[2] or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# RF-23: Log de Auditoria
@router.get("/admin/logs", response_model=List[LogAuditoria])
def listar_logs():
    """Lista logs de auditoria de ações sensíveis."""
    conn = get_db_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, usuario, acao, data FROM logs_auditoria ORDER BY data DESC LIMIT 100
        """)
        rows = cur.fetchall()
        return [LogAuditoria(id=row[0], usuario=row[1], acao=row[2], data=str(row[3])) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# Para integrar este módulo à aplicação principal, inclua:
# from .RF-20_23_ModuloAdministrativo import router as admin_router
# app.include_router(admin_router)
