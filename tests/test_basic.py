"""Basic tests for KimiClaw Business OS."""
import pytest
from kimiclaw.core.config import settings


def test_settings_loaded():
    """Test that settings can be loaded."""
    assert settings is not None
    assert settings.business_name is not None


def test_default_values():
    """Test default configuration values."""
    assert settings.business_capacity == 10
    assert settings.pricing_mode == "dynamic"
    assert settings.default_hourly_rate == 75.0


def test_database_models():
    """Test that database models can be imported."""
    from kimiclaw.models.database import Customer, Lead, Job, Invoice
    
    assert Customer is not None
    assert Lead is not None
    assert Job is not None
    assert Invoice is not None


def test_ollama_client():
    """Test that Ollama client can be imported."""
    from kimiclaw.integrations.ollama_client import OllamaClient
    
    client = OllamaClient()
    assert client is not None
    assert client.conversation_model == "llama3.2"


def test_api_server():
    """Test that FastAPI server can be created."""
    from kimiclaw.api.server import create_app
    
    app = create_app()
    assert app is not None
    assert app.title == "KimiClaw Business OS API"
