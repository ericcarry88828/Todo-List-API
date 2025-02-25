import os
from typing import Literal
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASEDIR = os.path.join(os.path.dirname(__file__), "../../")
ENV = os.getenv("ENV", "dev")
DOTENV = os.path.join(BASEDIR, ".env" if ENV == "dev" else "prod.env")


class DBSetting(BaseSettings):
    ENV: Literal["dev", "prod"] = ENV
    MYSQL_DRIVER: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD:  str
    MYSQL_DATABASE: str

    model_config = SettingsConfigDict(
        env_file=DOTENV,
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        base_url = (
            f"{self.MYSQL_DRIVER}://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )
        params = {
            "charset": "utf8mb4"
        }
        return f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"


settings = DBSetting()

if __name__ == "__main__":
    print(settings.DATABASE_URL)
