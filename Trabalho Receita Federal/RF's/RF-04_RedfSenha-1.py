from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class SolicitarRecuperacaoSchema(BaseModel):
    email: EmailStr

class ResetarSenhaSchema(BaseModel):
    token: str
    nova_senha: str = Field(..., min_length=8)

    @field_validator("nova_senha")
    @classmethod
    def validar_senha_forte(cls, v: str) -> str:
        # Exige: 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial
        padrao = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(padrao, v):
            raise ValueError(
                "A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, "
                "minúsculas, números e caracteres especiais."
            )
        return v