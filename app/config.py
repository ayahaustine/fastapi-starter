from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # app
    PROJECT_NAME: str
    API_VERSION: str
    DESCRIPTION: str
    ENVIRONMENT: str
    DEBUG: bool

    # security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # database
    DATABASE_URL: str
    DATABASE_TEST_URL: str | None = None

    # CORS
    BACKEND_CORS_ORIGINS: list[str]

    # redis
    REDIS_URL: str | None = "redis://localhost:6379/0"

    # email
    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
