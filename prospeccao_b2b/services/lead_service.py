"""Regras do funil de leads e permissoes por perfil."""

from models.company_model import CompanyModel
from models.lead_model import LeadModel, STATUS_LEAD


class LeadService:
    @staticmethod
    def criar_lead(cnpj, consultor_id, observacoes=""):
        # 1. So permite criar lead de empresa ja consultada/salva.
        empresa = CompanyModel.find_by_cnpj(cnpj)
        if not empresa:
            raise ValueError("Empresa nao encontrada. Consulte o CNPJ antes de criar o lead.")
        return LeadModel.create(empresa["id"], consultor_id, observacoes)

    @staticmethod
    def validar_acesso(lead, user):
        # 2. Lead inexistente nunca pode ser acessado.
        if not lead:
            return False

        # 3. Admin acessa todos; consultor acessa apenas os proprios.
        return user["perfil"] == "ADMIN" or lead["consultor_id"] == user["id"]

    @staticmethod
    def atualizar_status(lead_id, status, observacoes, user):
        # 4. Busca o lead e valida se o usuario pode altera-lo.
        lead = LeadModel.find_by_id(lead_id)
        if not LeadService.validar_acesso(lead, user):
            raise PermissionError("Voce nao tem permissao para alterar este lead.")
        if status not in STATUS_LEAD:
            raise ValueError("Status de lead invalido.")

        # 5. Atualiza status; observacao vazia vira None para preservar valor.
        return LeadModel.update_status(lead_id, status, observacoes or None)

    @staticmethod
    def remover(lead_id, user):
        # 6. Remove apenas depois de confirmar permissao no lead.
        lead = LeadModel.find_by_id(lead_id)
        if not LeadService.validar_acesso(lead, user):
            raise PermissionError("Voce nao tem permissao para remover este lead.")
        return LeadModel.delete(lead_id)
