"""
KimiClaw Business OS
Your AI. Your data. Your business.
🐝 Built for trades. Proven in Montreal.
"""

__version__ = "0.1.0"
__author__ = "KimiClaw Team"

from .core.config import settings
from .core.ollama_client import OllamaClient

__all__ = ["settings", "OllamaClient", "__version__"]
