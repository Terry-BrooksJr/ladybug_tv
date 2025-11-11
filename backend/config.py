"""Backend configuration"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/ladybug_tv"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    secret_key: str = "your-secret-key-change-in-production"
    
    # Stream
    stream_base_url: str = "http://localhost:8002"
    ffmpeg_path: str = "/usr/bin/ffmpeg"
    
    # EPG
    epg_update_interval: int = 3600
    
    class Config:
        env_file = ".env"

settings = Settings()
