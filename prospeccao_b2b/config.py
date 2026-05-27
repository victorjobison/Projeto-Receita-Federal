import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET", "dev-secret-change-me")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "prospeccao_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    BRASILAPI_URL = os.getenv("BRASILAPI_URL", "https://brasilapi.com.br/api/cnpj/v1")
    PAGE_SIZE = min(int(os.getenv("PAGE_SIZE", "50")), 50)
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@prospeccao.local")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    JWT_SECRET = os.getenv("JWT_SECRET", SECRET_KEY)
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
