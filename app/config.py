# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "local"
    database_url: str

    class Config:
        env_file = ".env.local"  # 開発中はこれ。デプロイ時に変えるor別ファイルに


settings = Settings()
