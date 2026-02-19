"""Redis client and customer memory utilities."""

import json
from typing import Optional, Dict, Any, List
import redis
from loguru import logger

from kimiclaw.core.config import settings
from kimiclaw.core.ollama_client import OllamaClient


class RedisClient:
    """Redis client for caching and customer memory."""
    
    def __init__(self):
        """Initialize Redis client."""
        self.client = redis.from_url(settings.redis_url, decode_responses=True)
        self.ollama = OllamaClient()
        
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set a key-value pair.
        
        Args:
            key: Cache key
            value: Value to store (will be JSON-encoded)
            expire: Optional expiration in seconds
            
        Returns:
            True if successful
        """
        try:
            serialized = json.dumps(value)
            if expire:
                return self.client.setex(key, expire, serialized)
            else:
                return self.client.set(key, serialized)
        except Exception as e:
            logger.error(f"Error setting Redis key {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value by key.
        
        Args:
            key: Cache key
            
        Returns:
            Deserialized value or None
        """
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting Redis key {key}: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete a key.
        
        Args:
            key: Cache key
            
        Returns:
            True if key was deleted
        """
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting Redis key {key}: {e}")
            return False
    
    async def store_customer_memory(
        self,
        customer_phone: str,
        interaction_text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store customer interaction in memory with embeddings.
        
        Args:
            customer_phone: Customer phone number
            interaction_text: Text of the interaction
            metadata: Optional metadata dict
            
        Returns:
            True if successful
        """
        try:
            # Generate embedding
            embedding = await self.ollama.embed(interaction_text)
            
            # Store interaction
            memory_key = f"customer_memory:{customer_phone}"
            memories = self.get(memory_key) or []
            
            memory_entry = {
                "text": interaction_text,
                "embedding": embedding,
                "metadata": metadata or {},
                "timestamp": str(datetime.utcnow())
            }
            
            memories.append(memory_entry)
            
            # Keep only last 50 memories per customer
            if len(memories) > 50:
                memories = memories[-50:]
            
            return self.set(memory_key, memories)
            
        except Exception as e:
            logger.error(f"Error storing customer memory: {e}")
            return False
    
    async def search_customer_memory(
        self,
        customer_phone: str,
        query: str,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Search customer memory using semantic similarity.
        
        Args:
            customer_phone: Customer phone number
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of most relevant memory entries
        """
        try:
            # Generate query embedding
            query_embedding = await self.ollama.embed(query)
            
            # Get customer memories
            memory_key = f"customer_memory:{customer_phone}"
            memories = self.get(memory_key) or []
            
            if not memories:
                return []
            
            # Calculate cosine similarity
            import numpy as np
            
            def cosine_similarity(a, b):
                return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            
            # Score each memory
            scored_memories = []
            for memory in memories:
                score = cosine_similarity(query_embedding, memory["embedding"])
                scored_memories.append({
                    "text": memory["text"],
                    "metadata": memory["metadata"],
                    "timestamp": memory["timestamp"],
                    "relevance_score": float(score)
                })
            
            # Sort by score and return top_k
            scored_memories.sort(key=lambda x: x["relevance_score"], reverse=True)
            return scored_memories[:top_k]
            
        except Exception as e:
            logger.error(f"Error searching customer memory: {e}")
            return []


# Global Redis client instance
redis_client = RedisClient()


from datetime import datetime
