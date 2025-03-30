import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "your-default-bot-token")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your-default-openai-key")
    AMPLITUDE_API_KEY: str = os.getenv("AMPLITUDE_API_KEY")

settings = Settings()
