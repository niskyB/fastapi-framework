import yaml
import sqlalchemy
from typing import List, Literal, Optional, Union
from pydantic import validator
from pydantic_settings import BaseSettings
from app.schemas.role import Role


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    ENV: Literal["prod", "stag", "dev"] = "dev"

    DB_SERVER: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_DB: Optional[str] = None
    DB_SCHEMA: Optional[str] = "public"

    TENANT_NAME: str = ""
    TENANT_ID: str = ""
    CLIENT_ID: str = ""
    CLIENT_SECRET: str = ""
    EXTENSION_APP_ID: str = ""

    ROLES_YML_FILE: str = "roles.yml"

    @property
    def EXTENSION_KEY_PREFIX(self):
        extension_app_id = self.EXTENSION_APP_ID.replace("-", "")
        return f"extension_{extension_app_id}"

    @property
    def SQLALCHEMY_DATABASE_URL(self):
        return sqlalchemy.engine.URL.create(
            "postgresql",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_SERVER,
            port=self.DB_PORT,
            database=self.DB_DB,
        )

    @property
    def USER_ROLES(self):
        with open(self.ROLES_YML_FILE, "r") as file:
            return Role(**yaml.safe_load(file)["user_roles"])

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
