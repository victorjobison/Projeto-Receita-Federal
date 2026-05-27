import uuid

from models.password_reset_model import PasswordResetModel
from models.user_model import UserModel
from utils.security import hash_password, verify_password


class AuthService:
    @staticmethod
    def authenticate(email, password):
        user = UserModel.find_by_email(email)
        if not user or not user["ativo"]:
            return None
        if not verify_password(password, user["senha_hash"]):
            return None
        return user

    @staticmethod
    def request_password_reset(email):
        user = UserModel.find_by_email(email)
        if not user or not user["ativo"]:
            return None

        token = uuid.uuid4().hex
        PasswordResetModel.create(user["id"], token)
        return token

    @staticmethod
    def reset_password(token, new_password):
        reset = PasswordResetModel.find_valid(token)
        if not reset:
            return False

        UserModel.update_password(reset["usuario_id"], hash_password(new_password))
        PasswordResetModel.mark_used(reset["id"])
        return True
