from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    news_api_key: str = ""
    database_url: str = "sqlite:///./diagnostic.db"
    secret_key: str = "change_me"
    environment: str = "development"
    s3_bucket: str = "ai-diagnostic-artifacts"
    aws_region: str = "us-east-1"

    # Model assignments per PRD
    model_opus: str = "claude-opus-4-7"
    model_sonnet: str = "claude-sonnet-4-6"
    model_haiku: str = "claude-haiku-4-5-20251001"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
