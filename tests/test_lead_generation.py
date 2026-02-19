"""Tests for lead generation module."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from kimiclaw.modules.lead_generation import LeadGenerationLoop


@pytest.mark.asyncio
async def test_score_lead_valid_response():
    """Test lead scoring with valid AI response."""
    loop = LeadGenerationLoop()
    
    # Mock Ollama client to return a score
    with patch('kimiclaw.modules.lead_generation.ollama_client') as mock_ollama:
        mock_ollama.generate = AsyncMock(return_value="85")
        
        score = await loop._score_lead({
            'name': 'Test Business',
            'business_type': 'property_management',
            'address': '123 Main St'
        })
        
        assert score == 85
        assert 0 <= score <= 100


@pytest.mark.asyncio
async def test_score_lead_no_digits():
    """Test lead scoring when AI returns no digits."""
    loop = LeadGenerationLoop()
    
    # Mock Ollama client to return non-numeric response
    with patch('kimiclaw.modules.lead_generation.ollama_client') as mock_ollama:
        mock_ollama.generate = AsyncMock(return_value="Unable to score")
        
        score = await loop._score_lead({
            'name': 'Test Business',
            'business_type': 'unknown'
        })
        
        # Should return default score
        assert score == 50


@pytest.mark.asyncio
async def test_score_lead_exception():
    """Test lead scoring when AI raises exception."""
    loop = LeadGenerationLoop()
    
    # Mock Ollama client to raise exception
    with patch('kimiclaw.modules.lead_generation.ollama_client') as mock_ollama:
        mock_ollama.generate = AsyncMock(side_effect=Exception("Connection error"))
        
        score = await loop._score_lead({
            'name': 'Test Business'
        })
        
        # Should return default score
        assert score == 50


@pytest.mark.asyncio
async def test_score_lead_boundary_values():
    """Test lead scoring boundary validation."""
    loop = LeadGenerationLoop()
    
    # Test values at and beyond boundaries
    test_cases = [
        ("0", 0),
        ("100", 100),
        ("150", 100),  # Should cap at 100
        ("-10", 0),    # Should floor at 0 (though extraction would skip negative)
    ]
    
    for response, expected in test_cases:
        with patch('kimiclaw.modules.lead_generation.ollama_client') as mock_ollama:
            mock_ollama.generate = AsyncMock(return_value=response)
            
            score = await loop._score_lead({'name': 'Test'})
            assert score == expected, f"Expected {expected} for response '{response}', got {score}"


@pytest.mark.asyncio
async def test_generate_opening_line():
    """Test opening line generation."""
    loop = LeadGenerationLoop()
    
    with patch('kimiclaw.modules.lead_generation.ollama_client') as mock_ollama:
        mock_ollama.generate = AsyncMock(
            return_value="Hi there, I noticed your business and thought we could help!"
        )
        
        opening = await loop._generate_opening_line({
            'name': 'Test Business',
            'business_type': 'retail'
        })
        
        assert isinstance(opening, str)
        assert len(opening) > 0


@pytest.mark.asyncio
async def test_generate_opening_line_exception():
    """Test opening line generation with exception."""
    loop = LeadGenerationLoop()
    
    with patch('kimiclaw.modules.lead_generation.ollama_client') as mock_ollama:
        mock_ollama.generate = AsyncMock(side_effect=Exception("AI error"))
        
        opening = await loop._generate_opening_line({'name': 'Test'})
        
        # Should return default message
        assert "I noticed your business" in opening
