"""Funcoes de hash e verificacao de senha com bcrypt."""

import bcrypt


MAX_BCRYPT_BYTES = 72


def _password_bytes(password: str) -> bytes:
    # 1. Converte senha para bytes, formato exigido pelo bcrypt.
    password_bytes = (password or "").encode("utf-8")

    # 2. bcrypt considera no maximo 72 bytes; rejeitamos antes de gerar hash.
    if len(password_bytes) > MAX_BCRYPT_BYTES:
        raise ValueError("A senha nao pode ultrapassar 72 bytes para bcrypt.")
    return password_bytes


def hash_password(password: str) -> str:
    # 3. Gera salt novo e devolve o hash como texto para salvar no banco.
    return bcrypt.hashpw(_password_bytes(password), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    # 4. Sem hash salvo, a senha nunca deve ser aceita.
    if not password_hash:
        return False
    try:
        # 5. Compara senha digitada com hash salvo sem expor a senha original.
        return bcrypt.checkpw(_password_bytes(password), password_hash.encode("utf-8"))
    except ValueError:
        # 6. Senha longa demais ou hash invalido resulta em autenticacao negada.
        return False
