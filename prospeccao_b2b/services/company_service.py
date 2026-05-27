"""Regras para consultar e listar empresas."""

import requests
from flask import current_app

from models.company_model import CompanyModel
from utils.formatters import only_numbers


class CompanyService:
    @staticmethod
    def consultar_cnpj(cnpj):
        # 1. Remove mascara/pontuacao e exige CNPJ com 14 digitos.
        cnpj_limpo = only_numbers(cnpj)
        if len(cnpj_limpo) != 14:
            raise ValueError("CNPJ invalido. Informe 14 numeros.")

        # 2. Chama a BrasilAPI usando a URL configurada no app.
        url = f"{current_app.config['BRASILAPI_URL']}/{cnpj_limpo}"
        response = requests.get(url, timeout=3)

        # 3. Transforma CNPJ inexistente em mensagem amigavel para a tela.
        if response.status_code == 404:
            raise ValueError("CNPJ nao encontrado na BrasilAPI.")

        # 4. Para outros erros HTTP, deixa requests levantar a excecao.
        response.raise_for_status()
        dados = response.json()

        # 5. Salva ou atualiza a empresa retornada pela API.
        return CompanyModel.upsert_from_api(dados)

    @staticmethod
    def listar_empresas(filters, consultor_id, page_size):
        # 6. Encaminha filtros para o model montar a consulta SQL.
        return CompanyModel.list_filtered(filters, consultor_id, page_size)
