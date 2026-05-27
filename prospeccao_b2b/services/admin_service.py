from collections import defaultdict

from models.lead_model import LeadModel, STATUS_LEAD
from models.user_model import UserModel
from utils.security import hash_password


class AdminService:
    @staticmethod
    def criar_consultor(nome, email, senha, perfil):
        return UserModel.create(nome, email, hash_password(senha), perfil)

    @staticmethod
    def editar_consultor(user_id, nome, email, perfil, ativo):
        return UserModel.update(user_id, nome, email, perfil, ativo)

    @staticmethod
    def relatorio_global():
        linhas = LeadModel.report_by_consultor_status()
        relatorio = defaultdict(lambda: {status: 0 for status in STATUS_LEAD})
        for row in linhas:
            consultor = row["consultor"]
            status = row["status"]
            relatorio[consultor]
            if status:
                relatorio[consultor][status] = row["total"]

        return [
            {
                "consultor": consultor,
                "status": totais,
                "total": sum(totais.values()),
            }
            for consultor, totais in relatorio.items()
        ]
