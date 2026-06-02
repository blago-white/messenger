from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class CommonSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def alembic_database_url(self) -> str:
        return (
            f"postgresql://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


class TestSettings(CommonSettings):
    POSTGRES_TEST_DB: str

    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_TEST_DB}"
        )


class Settings(CommonSettings):
    POSTGRES_DB: str

    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()
test_settings = TestSettings()
