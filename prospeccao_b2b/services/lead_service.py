from models.company_model import CompanyModel
from models.lead_model import LeadModel, STATUS_LEAD


class LeadService:
    @staticmethod
    def criar_lead(cnpj, consultor_id, observacoes=""):
        empresa = CompanyModel.find_by_cnpj(cnpj)
        if not empresa:
            raise ValueError("Empresa nao encontrada. Consulte o CNPJ antes de criar o lead.")
        return LeadModel.create(empresa["id"], consultor_id, observacoes)

    @staticmethod
    def validar_acesso(lead, user):
        if not lead:
            return False
        return user["perfil"] == "ADMIN" or lead["consultor_id"] == user["id"]

    @staticmethod
    def atualizar_status(lead_id, status, observacoes, user):
        lead = LeadModel.find_by_id(lead_id)
        if not LeadService.validar_acesso(lead, user):
            raise PermissionError("Voce nao tem permissao para alterar este lead.")
        if status not in STATUS_LEAD:
            raise ValueError("Status de lead invalido.")
        return LeadModel.update_status(lead_id, status, observacoes or None)

    @staticmethod
    def remover(lead_id, user):
        lead = LeadModel.find_by_id(lead_id)
        if not LeadService.validar_acesso(lead, user):
            raise PermissionError("Voce nao tem permissao para remover este lead.")
        return LeadModel.delete(lead_id)
