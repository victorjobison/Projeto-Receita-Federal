"""Regras de negocio da area administrativa."""

from collections import defaultdict

from models.lead_model import LeadModel, STATUS_LEAD
from models.user_model import UserModel
from utils.security import hash_password


class AdminService:
    @staticmethod
    def criar_consultor(nome, email, senha, perfil):
        # 1. Recebe senha em texto, gera hash e cria o usuario.
        return UserModel.create(nome, email, hash_password(senha), perfil)

    @staticmethod
    def editar_consultor(user_id, nome, email, perfil, ativo):
        # 2. Encaminha ao model a atualizacao dos campos administraveis.
        return UserModel.update(user_id, nome, email, perfil, ativo)

    @staticmethod
    def relatorio_global():
        # 3. Busca linhas agrupadas por consultor/status no banco.
        linhas = LeadModel.report_by_consultor_status()

        # 4. Garante que todos os status aparecam, mesmo quando o total for zero.
        relatorio = defaultdict(lambda: {status: 0 for status in STATUS_LEAD})
        for row in linhas:
            consultor = row["consultor"]
            status = row["status"]
            relatorio[consultor]
            if status:
                relatorio[consultor][status] = row["total"]

        # 5. Converte o dicionario em lista pronta para o template.
        return [
            {
                "consultor": consultor,
                "status": totais,
                "total": sum(totais.values()),
            }
            for consultor, totais in relatorio.items()
        ]
