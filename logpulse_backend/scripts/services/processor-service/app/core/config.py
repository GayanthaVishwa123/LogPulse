from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Default Redis URLs සෙට් කර තිබීමෙන් .env file එක නැතත් local dev වලදී crash නොවේ
    broker_url: str = "redis://localhost:6379/0"
    result_backend: str = "redis://localhost:6379/0"
    log_level: str = "info"

    # Pydantic v2 Settings Config Syntax
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # .env එකේ අමතර variables තිබුණත් errors නොදී ignore කරයි
    )


# App එක ඇතුළේ singleton instance එකක් විදිහට පාවිච්චි කිරීමට
settings = Settings()
