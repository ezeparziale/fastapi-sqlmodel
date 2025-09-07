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
    SUMMARY: str = ""
    DESCRIPTION: str = ""

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyHttpUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS]

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

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_TEST_DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOSTNAME + "_test",
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # pyright: ignore
