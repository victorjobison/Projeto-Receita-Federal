import requests
from flask import current_app

from models.company_model import CompanyModel
from utils.formatters import only_numbers


class CompanyService:
    @staticmethod
    def consultar_cnpj(cnpj):
        cnpj_limpo = only_numbers(cnpj)
        if len(cnpj_limpo) != 14:
            raise ValueError("CNPJ invalido. Informe 14 numeros.")

        url = f"{current_app.config['BRASILAPI_URL']}/{cnpj_limpo}"
        response = requests.get(url, timeout=3)
        if response.status_code == 404:
            raise ValueError("CNPJ nao encontrado na BrasilAPI.")

        response.raise_for_status()
        dados = response.json()
        return CompanyModel.upsert_from_api(dados)

    @staticmethod
    def listar_empresas(filters, consultor_id, page_size):
        return CompanyModel.list_filtered(filters, consultor_id, page_size)
