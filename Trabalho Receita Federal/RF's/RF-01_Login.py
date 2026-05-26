from fastapi import APIRouter, Depends, HTTPException, Response

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login")
async def login(response: Response, credenciais: LoginSchema): # LoginSchema exige e-mail válido
    # 1. Buscar usuário no banco pelo e-mail
    # 2. verificar_senha(credenciais.senha, usuario.senha_hash)
    # 3. Se falhar: raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    
    access_token = criar_token_acesso(data={"sub": str(usuario.id), "perfil": usuario.perfil})
    refresh_token = criar_token_acesso(data={"sub": str(usuario.id)}, expira_em_minutos=10080) # 7 dias
    
    # Define o cookie HTTPOnly para o Refresh Token (Segurança contra XSS)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True, # Usar TRUE em produção (HTTPS)
        samesite="lax",
        max_age=604800 # 7 dias em segundos
    )
    
    return {"access_token": access_token, "token_type": "bearer", "usuario": {"nome": usuario.nome}}