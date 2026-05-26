@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Sessão encerrada com sucesso. Limpe o token localmente."}