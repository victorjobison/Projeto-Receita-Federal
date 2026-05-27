"""Regras para criar, renovar e revogar tokens da API."""

from datetime import datetime, timedelta
import uuid

from flask import current_app
from jose import jwt

from models.refresh_token_model import RefreshTokenModel


class TokenService:
    @staticmethod
    def create_access_token(user):
        # 1. Monta payload com identidade, perfil e expiracao curta.
        payload = {
            "sub": str(user["id"]),
            "nome": user["nome"],
            "email": user["email"],
            "perfil": user["perfil"],
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }

        # 2. Assina o JWT usando segredo e algoritmo configurados.
        return jwt.encode(
            payload,
            current_app.config["JWT_SECRET"],
            algorithm=current_app.config["JWT_ALGORITHM"],
        )

    @staticmethod
    def create_refresh_token(user_id):
        # 3. Gera token opaco, salva no banco e devolve ao cliente.
        token = uuid.uuid4().hex
        RefreshTokenModel.create(user_id, token)
        return token

    @staticmethod
    def refresh_access_token(refresh_token):
        # 4. Valida refresh token antes de emitir novo access token.
        user = RefreshTokenModel.find_valid(refresh_token)
        if not user:
            return None
        return TokenService.create_access_token(user)

    @staticmethod
    def revoke_refresh_token(refresh_token):
        # 5. Revoga o refresh token para impedir novas renovacoes.
        return RefreshTokenModel.revoke(refresh_token)
