import os
from dotenv import load_dotenv

# 🔹 Carrega as variáveis do arquivo .env
load_dotenv()

class Config:
    """Configurações gerais"""
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
    HOST = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    PORT = int(os.getenv("FLASK_RUN_PORT", 5000))
    # 🔹 Chave do reCAPTCHA
    RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")
    # 🔹 Carregar usuários e senhas do .env (convertendo para dicionário)
    USERS = {
        user.split(":")[0]: user.split(":")[1]
        for user in os.getenv("USERS", "").split(",") if ":" in user
    }

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
