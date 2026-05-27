from decimal import Decimal
import re


def only_numbers(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def decimal_or_zero(value) -> Decimal:
    try:
        return Decimal(str(value or "0").replace(",", "."))
    except Exception:
        return Decimal("0")


def normalize_status(value: str) -> str:
    return (value or "").strip().upper()
