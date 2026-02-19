"""Ollama client wrapper for KimiClaw Business OS."""

import asyncio
from typing import Optional, Dict, Any, List
import httpx
from loguru import logger

from .config import settings


class OllamaClient:
    """Client for interacting with Ollama AI models."""
    
    def __init__(self, host: Optional[str] = None):
        """Initialize Ollama client.
        
        Args:
            host: Ollama server host URL
        """
        self.host = host or settings.ollama_host
        self.conversation_model = settings.ollama_conversation_model
        self.reasoning_model = settings.ollama_reasoning_model
        self.vision_model = settings.ollama_vision_model
        self.embedding_model = settings.ollama_embedding_model
        
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        context: Optional[List[int]] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """Generate a response from Ollama.
        
        Args:
            prompt: The prompt to send to the model
            model: Model name (defaults to conversation model)
            system: System prompt
            context: Previous conversation context
            temperature: Sampling temperature
            
        Returns:
            Response dictionary with 'response' and 'context' keys
        """
        model = model or self.conversation_model
        
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False,
        }
        
        if system:
            payload["system"] = system
        if context:
            payload["context"] = context
            
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.host}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error generating response from Ollama: {e}")
            raise
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """Have a chat conversation with Ollama.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (defaults to conversation model)
            temperature: Sampling temperature
            
        Returns:
            Response dictionary
        """
        model = model or self.conversation_model
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.host}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error in chat with Ollama: {e}")
            raise
    
    async def analyze_image(
        self,
        image_base64: str,
        prompt: str,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Analyze an image using vision model.
        
        Args:
            image_base64: Base64-encoded image
            prompt: Prompt describing what to analyze
            model: Model name (defaults to vision model)
            
        Returns:
            Analysis response
        """
        if not settings.is_full_mode:
            return {
                "error": "Image analysis requires Full Mode (16GB+ RAM)",
                "response": "System is in Lite Mode. Image analysis unavailable."
            }
        
        model = model or self.vision_model
        
        payload = {
            "model": model,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False,
        }
        
        try:
            async with httpx.AsyncClient(timeout=180.0) as client:
                response = await client.post(
                    f"{self.host}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error analyzing image with Ollama: {e}")
            raise
    
    async def embed(
        self,
        text: str,
        model: Optional[str] = None,
    ) -> List[float]:
        """Generate embeddings for text.
        
        Args:
            text: Text to embed
            model: Model name (defaults to embedding model)
            
        Returns:
            List of embedding values
        """
        model = model or self.embedding_model
        
        payload = {
            "model": model,
            "prompt": text,
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.host}/api/embeddings",
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                return result.get("embedding", [])
        except Exception as e:
            logger.error(f"Error generating embeddings with Ollama: {e}")
            raise
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List available models in Ollama.
        
        Returns:
            List of model information dictionaries
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.host}/api/tags")
                response.raise_for_status()
                result = response.json()
                return result.get("models", [])
        except Exception as e:
            logger.error(f"Error listing Ollama models: {e}")
            raise
    
    async def pull_model(self, model: str) -> bool:
        """Pull a model from Ollama registry.
        
        Args:
            model: Model name to pull
            
        Returns:
            True if successful
        """
        payload = {"name": model, "stream": False}
        
        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                response = await client.post(
                    f"{self.host}/api/pull",
                    json=payload
                )
                response.raise_for_status()
                logger.info(f"Successfully pulled model: {model}")
                return True
        except Exception as e:
            logger.error(f"Error pulling model {model}: {e}")
            raise
