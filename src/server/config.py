import os

from dotenv import load_dotenv


dotenv_path = './src/.env'
load_dotenv(dotenv_path)


class Config:
    """Настройки проекта."""

    DEBUG = os.environ.get('DEBUG', False) in {'True', 'true', '1', True}
    RELOAD = os.environ.get('RELOAD', False) in {'True', 'true', '1', True}
    APP_HOST = os.environ.get('APP_HOST', '127.0.0.1')
    APP_PORT = int(os.environ.get('APP_PORT', '8000'))

    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
    POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', 5432))
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'ws')
    DB_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key')
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
    IS_PROXY = os.environ.get('IS_PROXY', False) in {'True', 'true', '1', True}
    FAKE_ECHO_SERVER = 'wss://echo.websocket.org'
