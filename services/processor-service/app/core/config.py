from pydantic import BaseSettings


class Settings(BaseSettings):
    broker_url: str
    result_backend: str
    log_level: str = "info"

    class Config:
        env_file = ".env"
