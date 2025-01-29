import os
from typing import Optional
from openai import OpenAI
from pydantic_settings import BaseSettings


class OpenAIConfig:
    def __init__(self):
        self.API_KEY: Optional[str] = os.environ.get("OPENAI_API_KEY")

    def setup(self) -> OpenAI:
        if not self.API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required.")
        return OpenAI(api_key=self.API_KEY)


class Settings(BaseSettings):
    APP_NAME: str = "Review App"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    REDIS_URL: str = os.environ.get("REDIS_URL")

    openai: OpenAIConfig = OpenAIConfig()


# Initialize settings
settings = Settings()

# Initialize OpenAI client
openai_client = settings.openai.setup()
