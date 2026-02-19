"""Tests for Ollama client."""

import pytest
from unittest.mock import AsyncMock, patch
from kimiclaw.core.ollama_client import OllamaClient


@pytest.fixture
def ollama_client():
    """Create an Ollama client for testing."""
    return OllamaClient(host="http://localhost:11434")


@pytest.mark.asyncio
async def test_generate(ollama_client):
    """Test generate method."""
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "response": "Hello, how can I help you?",
            "context": [1, 2, 3]
        }
        mock_response.raise_for_status = AsyncMock()
        mock_post.return_value.__aenter__.return_value = mock_response
        
        result = await ollama_client.generate(
            prompt="Hello",
            temperature=0.7
        )
        
        assert "response" in result
        assert result["response"] == "Hello, how can I help you?"


@pytest.mark.asyncio
async def test_chat(ollama_client):
    """Test chat method."""
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "message": {"role": "assistant", "content": "Hello!"}
        }
        mock_response.raise_for_status = AsyncMock()
        mock_post.return_value.__aenter__.return_value = mock_response
        
        messages = [
            {"role": "user", "content": "Hello"}
        ]
        
        result = await ollama_client.chat(messages=messages)
        
        assert "message" in result


@pytest.mark.asyncio
async def test_embed(ollama_client):
    """Test embedding generation."""
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "embedding": [0.1, 0.2, 0.3, 0.4]
        }
        mock_response.raise_for_status = AsyncMock()
        mock_post.return_value.__aenter__.return_value = mock_response
        
        result = await ollama_client.embed(text="Test text")
        
        assert isinstance(result, list)
        assert len(result) == 4
