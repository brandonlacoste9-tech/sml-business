"""Lead Generation Loop - autonomous lead hunting and scoring."""

import asyncio
from datetime import datetime
from loguru import logger

from kimiclaw.core.config import settings
from kimiclaw.core.ollama_client import OllamaClient


class LeadGenerationLoop:
    """Autonomous lead generation system."""
    
    def __init__(self):
        self.ollama = OllamaClient()
        self.last_hunt = None
        
    async def start(self):
        """Start the lead generation loop."""
        logger.info("🔍 Lead Generation Loop started")
        
        while True:
            try:
                # Check if it's time for daily hunt (default 8am)
                if await self.should_run_daily_hunt():
                    await self.run_daily_hunt()
                
                await asyncio.sleep(3600)  # Check every hour
                
            except asyncio.CancelledError:
                logger.info("Lead Generation Loop stopped")
                break
            except Exception as e:
                logger.error(f"Error in Lead Generation Loop: {e}")
                await asyncio.sleep(300)
    
    async def should_run_daily_hunt(self) -> bool:
        """Check if it's time to run the daily lead hunt."""
        now = datetime.now()
        
        # If never run, run it
        if self.last_hunt is None:
            return True
        
        # If last run was yesterday or earlier, and it's past 8am
        if self.last_hunt.date() < now.date() and now.hour >= 8:
            return True
        
        return False
    
    async def run_daily_hunt(self):
        """Run the daily lead hunting process."""
        logger.info("🎯 Starting daily lead hunt")
        
        try:
            # Search for leads
            leads = await self.search_leads()
            
            # Score leads
            scored_leads = []
            for lead in leads:
                score = await self.score_lead(lead)
                lead["score"] = score
                scored_leads.append(lead)
            
            # Sort by score
            scored_leads.sort(key=lambda x: x["score"], reverse=True)
            
            # Filter hot leads (score >= 70)
            hot_leads = [l for l in scored_leads if l["score"] >= settings.lead_score_threshold]
            
            logger.info(f"Found {len(leads)} leads, {len(hot_leads)} are hot (score >= {settings.lead_score_threshold})")
            
            # Generate opening lines for hot leads
            for lead in hot_leads:
                opening_line = await self.generate_opening_line(lead)
                lead["opening_line"] = opening_line
            
            # TODO: Save leads to database
            # TODO: Send WhatsApp summary to owner
            
            self.last_hunt = datetime.now()
            
        except Exception as e:
            logger.error(f"Error in daily lead hunt: {e}")
    
    async def search_leads(self) -> list:
        """Search for potential leads.
        
        Returns:
            List of lead dictionaries
        """
        # TODO: Implement actual lead search via SerpAPI
        # This is a placeholder
        return [
            {
                "business_name": "Example Property Management",
                "address": "123 Main St, Montreal, QC",
                "phone": "+15145551234",
                "source": "google_maps",
                "type": "commercial_property"
            }
        ]
    
    async def score_lead(self, lead: dict) -> int:
        """Score a lead from 0-100.
        
        Args:
            lead: Lead data dictionary
            
        Returns:
            Score from 0 to 100
        """
        try:
            # Use Ollama reasoning model to score the lead
            prompt = f"""
            Score this potential customer lead for a {settings.business_industry} business from 0-100.
            
            Lead Information:
            - Business: {lead.get('business_name', 'Unknown')}
            - Type: {lead.get('type', 'Unknown')}
            - Address: {lead.get('address', 'Unknown')}
            - Source: {lead.get('source', 'Unknown')}
            
            Consider:
            - Relevance to our industry
            - Urgency signals
            - Business type and size
            - Location proximity
            
            Return only the numeric score (0-100).
            """
            
            response = await self.ollama.generate(
                prompt=prompt,
                model=settings.ollama_reasoning_model,
                temperature=0.3
            )
            
            score_text = response.get("response", "50").strip()
            
            # Extract numeric score
            import re
            match = re.search(r'\d+', score_text)
            if match:
                score = int(match.group())
                return max(0, min(100, score))  # Clamp to 0-100
            
            return 50  # Default score
            
        except Exception as e:
            logger.error(f"Error scoring lead: {e}")
            return 50
    
    async def generate_opening_line(self, lead: dict) -> str:
        """Generate a personalized opening line for outreach.
        
        Args:
            lead: Lead data dictionary
            
        Returns:
            Personalized opening line
        """
        try:
            prompt = f"""
            Generate a brief, personalized opening line for reaching out to this potential customer.
            
            Our business: {settings.business_name} - {settings.business_industry}
            Lead: {lead.get('business_name', 'Unknown')}
            
            Keep it professional, friendly, and specific to their business.
            Maximum 2 sentences.
            """
            
            response = await self.ollama.generate(
                prompt=prompt,
                model=settings.ollama_conversation_model,
                temperature=0.7
            )
            
            return response.get("response", "").strip()
            
        except Exception as e:
            logger.error(f"Error generating opening line: {e}")
            return "Hi, I noticed your business and thought we could help."
