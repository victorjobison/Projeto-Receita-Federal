from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

async def obter_usuario_atual(token: str = Depends(oauth2_scheme)):
    excecao_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise excecao_credenciais
    except JWTError:
        raise excecao_credenciais
    
    # Aqui entraria a chamada ao banco (PostgreSQL) para verificar se o usuário ainda está ATIVO
    # usuario = await db.fetch_val_query("SELECT id, nome, perfil FROM usuarios WHERE id = $1 AND ativo = TRUE", usuario_id)
    # if not usuario: raise excecao_credenciais
    
    return payload # Retorna os dados do usuário injetados na rota