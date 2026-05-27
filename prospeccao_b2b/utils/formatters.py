"""Funcoes auxiliares para limpar e converter dados de entrada."""

from decimal import Decimal
import re


def only_numbers(value: str) -> str:
    # 1. Remove tudo que nao for digito, util para CNPJ e documentos.
    return re.sub(r"\D", "", value or "")


def decimal_or_zero(value) -> Decimal:
    # 2. Converte textos numericos para Decimal, aceitando virgula decimal.
    try:
        return Decimal(str(value or "0").replace(",", "."))
    except Exception:
        # 3. Entrada invalida vira zero para evitar quebra em filtros/salvamento.
        return Decimal("0")


def normalize_status(value: str) -> str:
    # 4. Padroniza texto de status para comparacoes simples.
    return (value or "").strip().upper()
