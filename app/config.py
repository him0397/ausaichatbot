import os
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env='OPENAI_API_KEY')
    print(openai_api_key)
    class Config:
        extra = "allow" 
        env_file = ".env"

settings = Settings()
