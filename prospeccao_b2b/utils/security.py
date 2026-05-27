import bcrypt


MAX_BCRYPT_BYTES = 72


def _password_bytes(password: str) -> bytes:
    password_bytes = (password or "").encode("utf-8")
    if len(password_bytes) > MAX_BCRYPT_BYTES:
        raise ValueError("A senha nao pode ultrapassar 72 bytes para bcrypt.")
    return password_bytes


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_password_bytes(password), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash:
        return False
    try:
        return bcrypt.checkpw(_password_bytes(password), password_hash.encode("utf-8"))
    except ValueError:
        return False
