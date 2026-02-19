"""KimiClaw Business OS - Configuration Management"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Business Information
    business_name: str = Field(default="Your Business Name", env="BUSINESS_NAME")
    business_industry: str = Field(default="plumbing", env="BUSINESS_INDUSTRY")
    business_phone: Optional[str] = Field(default=None, env="BUSINESS_PHONE")
    business_whatsapp: Optional[str] = Field(default=None, env="BUSINESS_WHATSAPP")
    business_hours_start: str = Field(default="08:00", env="BUSINESS_HOURS_START")
    business_hours_end: str = Field(default="18:00", env="BUSINESS_HOURS_END")
    business_capacity: int = Field(default=10, env="BUSINESS_CAPACITY")
    business_language: str = Field(default="en", env="BUSINESS_LANGUAGE")
    
    # Database
    database_url: str = Field(default="postgresql://kimiclaw:password@localhost:5432/kimiclaw", env="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Ollama Configuration
    ollama_host: str = Field(default="http://localhost:11434", env="OLLAMA_HOST")
    ollama_conversation_model: str = Field(default="llama3.2", env="OLLAMA_CONVERSATION_MODEL")
    ollama_reasoning_model: str = Field(default="mistral", env="OLLAMA_REASONING_MODEL")
    ollama_vision_model: str = Field(default="llava:13b", env="OLLAMA_VISION_MODEL")
    ollama_embedding_model: str = Field(default="nomic-embed-text", env="OLLAMA_EMBEDDING_MODEL")
    
    # External Services
    twilio_account_sid: Optional[str] = Field(default=None, env="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[str] = Field(default=None, env="TWILIO_AUTH_TOKEN")
    twilio_phone_number: Optional[str] = Field(default=None, env="TWILIO_PHONE_NUMBER")
    
    serpapi_key: Optional[str] = Field(default=None, env="SERPAPI_KEY")
    
    google_calendar_credentials_path: Optional[str] = Field(default=None, env="GOOGLE_CALENDAR_CREDENTIALS_PATH")
    google_gmail_credentials_path: Optional[str] = Field(default=None, env="GOOGLE_GMAIL_CREDENTIALS_PATH")
    
    quickbooks_client_id: Optional[str] = Field(default=None, env="QUICKBOOKS_CLIENT_ID")
    quickbooks_client_secret: Optional[str] = Field(default=None, env="QUICKBOOKS_CLIENT_SECRET")
    stripe_api_key: Optional[str] = Field(default=None, env="STRIPE_API_KEY")
    
    # Application Settings
    app_port: int = Field(default=3000, env="APP_PORT")
    api_port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Pricing Configuration
    pricing_mode: str = Field(default="dynamic", env="PRICING_MODE")
    default_hourly_rate: float = Field(default=75.0, env="DEFAULT_HOURLY_RATE")
    surge_pricing_multiplier: float = Field(default=1.3, env="SURGE_PRICING_MULTIPLIER")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
