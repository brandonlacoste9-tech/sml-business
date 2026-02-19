"""Configuration management for KimiClaw Business OS."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Business Information
    business_name: str = "Your Business"
    business_industry: str = "general"
    business_language: str = "en"
    business_phone: str = ""
    business_whatsapp: str = ""
    
    # Operating Hours
    business_hours_start: str = "08:00"
    business_hours_end: str = "17:00"
    business_timezone: str = "America/Toronto"
    
    # Capacity & Mode Settings
    weekly_capacity: int = 40
    hunter_mode_threshold: float = 0.6
    surge_mode_threshold: float = 0.9
    
    # Database
    database_url: str = "postgresql://kimiclaw:password@localhost:5432/kimiclaw"
    redis_url: str = "redis://localhost:6379/0"
    
    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_conversation_model: str = "llama3.2"
    ollama_reasoning_model: str = "mistral"
    ollama_vision_model: str = "llava:13b"
    ollama_embedding_model: str = "nomic-embed-text"
    
    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""
    
    # Google
    google_credentials_path: str = "credentials/google-credentials.json"
    google_calendar_id: str = ""
    google_gmail_address: str = ""
    
    # Lead Generation
    serpapi_key: str = ""
    lead_hunt_schedule: str = "0 8 * * *"
    lead_score_threshold: int = 70
    
    # Advertising
    ad_schedule_morning: str = "0 9 * * *"
    ad_schedule_afternoon: str = "0 15 * * *"
    
    # Financial
    stripe_api_key: str = ""
    quickbooks_client_id: str = ""
    quickbooks_client_secret: str = ""
    
    # System Mode
    system_mode: str = "lite"  # lite or full
    auto_send_emails: bool = False
    emergency_keywords: str = "flood,fire,sparks,no heat,gas leak,urgent"
    
    # Webhook URL
    webhook_base_url: str = "http://localhost:8000"
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def emergency_keywords_list(self) -> list[str]:
        """Get emergency keywords as a list."""
        return [k.strip().lower() for k in self.emergency_keywords.split(",")]
    
    @property
    def is_full_mode(self) -> bool:
        """Check if system is running in full mode."""
        return self.system_mode.lower() == "full"
    
    def detect_system_mode(self) -> str:
        """Auto-detect system mode based on available RAM."""
        try:
            import psutil
            total_ram_gb = psutil.virtual_memory().total / (1024**3)
            return "full" if total_ram_gb >= 16 else "lite"
        except ImportError:
            return "lite"


# Global settings instance
settings = Settings()
