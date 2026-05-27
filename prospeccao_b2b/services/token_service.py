from datetime import datetime, timedelta
import uuid

from flask import current_app
from jose import jwt

from models.refresh_token_model import RefreshTokenModel


class TokenService:
    @staticmethod
    def create_access_token(user):
        payload = {
            "sub": str(user["id"]),
            "nome": user["nome"],
            "email": user["email"],
            "perfil": user["perfil"],
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }
        return jwt.encode(
            payload,
            current_app.config["JWT_SECRET"],
            algorithm=current_app.config["JWT_ALGORITHM"],
        )

    @staticmethod
    def create_refresh_token(user_id):
        token = uuid.uuid4().hex
        RefreshTokenModel.create(user_id, token)
        return token

    @staticmethod
    def refresh_access_token(refresh_token):
        user = RefreshTokenModel.find_valid(refresh_token)
        if not user:
            return None
        return TokenService.create_access_token(user)

    @staticmethod
    def revoke_refresh_token(refresh_token):
        return RefreshTokenModel.revoke(refresh_token)
