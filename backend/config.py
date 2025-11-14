"""Backend configuration"""
from pydantic_settings import BaseSettings
import os
import dotenv

dotenv.load_dotenv()
class Settings(BaseSettings):
    # Database
    database_url: str = os.environ.get("DATABASE_URl")
    
    # Redis
    redis_url: str = os.environ.get("REDIS_URL")
    
    # API
    api_host: str = os.environ.get("API_HOST")
    api_port: int = os.environ.get("API_PORT", 8000)
    secret_key: str = os.environ.get("SECRET_KEY")
    
    # Stream
    stream_base_url: str = "http://localhost:8002"
    ffmpeg_path: str = "/usr/bin/ffmpeg"
    
    # EPG
    epg_update_interval: int = 3600
    
    class Config:
        env_file = ".envrc"

settings = Settings()
