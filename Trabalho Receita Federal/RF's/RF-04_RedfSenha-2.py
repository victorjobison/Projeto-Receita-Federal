# routers/auth.py (Continuação)
from fastapi import APIRouter, HTTPException, status
from security import criar_token_acesso, gerar_hash_senha
from jose import jwt, JWTError
import os

# Endpoint 1: Solicitação de recuperação
@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def esqueci_senha(dados: SolicitarRecuperacaoSchema):
    # 1. Buscar o usuário no banco pelo e-mail
    # usuario = await db.buscar_por_email(dados.email)
    
    # Segurança: Mesmo se o e-mail não existir, retorne 200 para evitar que hackers descubram e-mails válidos
    # if not usuario: return {"message": "Se o e-mail existir, um link de recuperação será enviado."}
    
    # 2. Gerar um token JWT de curta duração (1 hora) exclusivo para password reset
    token_recuperacao = criar_token_acesso(
        dados={"sub": "usuario.id", "scope": "password_reset"}, 
        expira_em_minutos=60
    )
    
    link_seguro = f"https://meusaas.com.br/reset-password?token={token_recuperacao}"
    
    # 3. Chamar a sua função/serviço de e-mail (ex: SendGrid/SMTP)
    # await enviar_email_recuperacao(dados.email, link_seguro)
    
    return {"message": "E-mail de recuperação enviado com sucesso."}


# Endpoint 2: Redefinição da senha através do link
@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def resetar_senha(dados: ResetarSenhaSchema):
    try:
        # Decodifica e valida o tempo de vida do token (se passar de 1h dá erro automaticamente)
        payload = jwt.decode(dados.token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        
        # Garante que esse token só serve para resetar senha, impedindo reuso ilícito como login
        if payload.get("scope") != "password_reset":
            raise HTTPException(status_code=400, detail="Token inválido para esta operação.")
            
        usuario_id = payload.get("sub")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="O link de recuperação expirou ou é inválido.")
    
    # 3. Gerar o hash seguro da nova senha validada pelo Pydantic
    nova_senha_criptografada = gerar_hash_senha(dados.nova_senha)
    
    # 4. Atualizar no banco de dados
    # await db.update_password(usuario_id, nova_senha_criptografada)
    
    # 5. Enviar e-mail de confirmação de alteração por segurança
    # await enviar_email_confirmacao(usuario_email)
    
    return {"message": "Senha alterada com sucesso!"}