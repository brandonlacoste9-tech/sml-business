"""Ollama AI integration layer for local AI inference."""
import ollama
from typing import Optional, List, Dict, Any
from kimiclaw.core.config import settings
import logging

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama local AI models."""
    
    def __init__(self):
        self.host = settings.ollama_host
        self.conversation_model = settings.ollama_conversation_model
        self.reasoning_model = settings.ollama_reasoning_model
        self.vision_model = settings.ollama_vision_model
        self.embedding_model = settings.ollama_embedding_model
        
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Generate a chat response using the specified model.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (defaults to conversation model)
            system_prompt: Optional system prompt to prepend
            temperature: Sampling temperature (0.0-1.0)
            
        Returns:
            Generated response text
        """
        if model is None:
            model = self.conversation_model
            
        try:
            # Prepend system prompt if provided
            if system_prompt:
                messages = [{"role": "system", "content": system_prompt}] + messages
            
            response = ollama.chat(
                model=model,
                messages=messages,
                options={"temperature": temperature}
            )
            
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            raise
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text completion using the specified model.
        
        Args:
            prompt: Input prompt
            model: Model to use (defaults to conversation model)
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0.0-1.0)
            
        Returns:
            Generated text
        """
        if model is None:
            model = self.conversation_model
            
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            response = ollama.generate(
                model=model,
                prompt=full_prompt,
                options={"temperature": temperature}
            )
            
            return response['response']
        except Exception as e:
            logger.error(f"Ollama generate error: {e}")
            raise
    
    async def analyze_image(
        self,
        image_path: str,
        prompt: str,
        model: Optional[str] = None
    ) -> str:
        """
        Analyze an image using vision model.
        
        Args:
            image_path: Path to image file
            prompt: Question/instruction about the image
            model: Vision model to use (defaults to configured vision model)
            
        Returns:
            Analysis results
        """
        if model is None:
            model = self.vision_model
            
        try:
            response = ollama.chat(
                model=model,
                messages=[{
                    "role": "user",
                    "content": prompt,
                    "images": [image_path]
                }]
            )
            
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama vision error: {e}")
            raise
    
    async def embed(
        self,
        text: str,
        model: Optional[str] = None
    ) -> List[float]:
        """
        Generate embeddings for text.
        
        Args:
            text: Input text
            model: Embedding model to use (defaults to configured embedding model)
            
        Returns:
            Embedding vector
        """
        if model is None:
            model = self.embedding_model
            
        try:
            response = ollama.embeddings(
                model=model,
                prompt=text
            )
            
            return response['embedding']
        except Exception as e:
            logger.error(f"Ollama embedding error: {e}")
            raise
    
    def check_health(self) -> Dict[str, Any]:
        """
        Check Ollama service health and available models.
        
        Returns:
            Health status dict
        """
        try:
            models = ollama.list()
            return {
                "status": "healthy",
                "host": self.host,
                "models": [m['name'] for m in models.get('models', [])]
            }
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# Global client instance
ollama_client = OllamaClient()
