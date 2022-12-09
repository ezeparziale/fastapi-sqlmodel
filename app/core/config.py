from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    # FastAPI
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI + SQLModel"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database
    POSTGRES_HOSTNAME: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_TEST_PORT: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOSTNAME"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SQLALCHEMY_TEST_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_TEST_DATABASE_URI", pre=True)
    def assemble_db_test_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOSTNAME") + "_test",
            port=values.get("POSTGRES_TEST_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        env_file = ".env"


settings = Settings()
