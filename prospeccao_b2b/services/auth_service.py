"""Regras de autenticacao, recuperacao e troca de senha."""

import uuid

from models.password_reset_model import PasswordResetModel
from models.user_model import UserModel
from utils.security import hash_password, verify_password


class AuthService:
    @staticmethod
    def authenticate(email, password):
        # 1. Busca usuario pelo e-mail informado.
        user = UserModel.find_by_email(email)

        # 2. Recusa login se o usuario nao existir ou estiver inativo.
        if not user or not user["ativo"]:
            return None

        # 3. Compara senha digitada com o hash salvo no banco.
        if not verify_password(password, user["senha_hash"]):
            return None

        # 4. Retorna o usuario para controller gravar na sessao ou gerar JWT.
        return user

    @staticmethod
    def request_password_reset(email):
        # 5. Busca usuario ativo para gerar link de recuperacao.
        user = UserModel.find_by_email(email)
        if not user or not user["ativo"]:
            return None

        # 6. Gera token aleatorio e salva com prazo de expiracao.
        token = uuid.uuid4().hex
        PasswordResetModel.create(user["id"], token)
        return token

    @staticmethod
    def reset_password(token, new_password):
        # 7. Confere se o token existe, ainda vale e nao foi usado.
        reset = PasswordResetModel.find_valid(token)
        if not reset:
            return False

        # 8. Atualiza a senha com hash e invalida o token logo depois.
        UserModel.update_password(reset["usuario_id"], hash_password(new_password))
        PasswordResetModel.mark_used(reset["id"])
        return True
