from fastapi import Request

@router.post("/refresh")
async def atualizar_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token ausente")
    
    # 1. Validar o refresh_token com o REFRESH_SECRET_KEY
    # 2. Gerar novo access_token
    # 3. Retornar novo access_token