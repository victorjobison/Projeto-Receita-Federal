from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha) # Bcrypt já aplica salt automaticamente (rounds padrão = 12)

def criar_token_acesso(dados: dict, expira_em_minutos: int = 30):
    to_encode = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=expira_em_minutos)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)