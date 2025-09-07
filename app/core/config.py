from typing import Annotated, Any, Literal

from pydantic import AnyHttpUrl, BeforeValidator, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    # FastAPI
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI + SQLModel"
    SUMMARY: str = "A robust and modern backend with FastAPI and SQLModel."
    DESCRIPTION: str = (
        "This project is a production-ready template for building APIs. It leverages "
        "the high performance of FastAPI, the simplicity and power of SQLModel for "
        "database interactions (combining Pydantic and SQLAlchemy), and follows best "
        "practices for project structure and dependency management."
    )

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyHttpUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).strip("/") for origin in self.BACKEND_CORS_ORIGINS]

    # Database
    POSTGRES_HOSTNAME: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOSTNAME,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    # Database test
    POSTGRES_HOSTNAME_TEST: str
    POSTGRES_PORT_TEST: int = 5432
    POSTGRES_USER_TEST: str
    POSTGRES_PASSWORD_TEST: str
    POSTGRES_DB_TEST: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_TEST_DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER_TEST,
            password=self.POSTGRES_PASSWORD_TEST,
            host=self.POSTGRES_HOSTNAME_TEST,
            port=self.POSTGRES_PORT_TEST,
            path=self.POSTGRES_DB_TEST,
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # pyright: ignore
