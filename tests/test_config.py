"""Tests for KimiClaw configuration."""

import pytest
from kimiclaw.core.config import Settings


def test_settings_defaults():
    """Test that settings have sensible defaults."""
    settings = Settings()
    
    assert settings.business_name == "Your Business"
    assert settings.business_industry == "general"
    assert settings.business_language == "en"
    assert settings.system_mode in ["lite", "full"]


def test_emergency_keywords_list():
    """Test emergency keywords parsing."""
    settings = Settings(emergency_keywords="flood,fire,urgent")
    
    keywords = settings.emergency_keywords_list
    assert "flood" in keywords
    assert "fire" in keywords
    assert "urgent" in keywords
    assert len(keywords) == 3


def test_is_full_mode():
    """Test full mode detection."""
    settings_lite = Settings(system_mode="lite")
    assert not settings_lite.is_full_mode
    
    settings_full = Settings(system_mode="full")
    assert settings_full.is_full_mode
