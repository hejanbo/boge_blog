from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = 'prod'
    SERVER_HOST: str = '127.0.0.1'
    SERVER_PORT: int = 8000

    DATABASE_URL: str = ''

    SMTP_SERVER: str = ''
    SMTP_PORT: int = 465
    SMTP_USER: str = ''
    SMTP_PASS: str = ''

    SECURITY_KEY: str = ''
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    JWT_ISS: str = 'bogeblog'
    JWT_AUD: str = 'web'

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}