"""Lead Generation Loop - Hunts for new leads daily at 8am."""
import asyncio
import logging
from datetime import datetime, time
from kimiclaw.core.database import get_db
from kimiclaw.models.database import Lead
from kimiclaw.integrations.ollama_client import ollama_client
from kimiclaw.core.config import settings

logger = logging.getLogger(__name__)


class LeadGenerationLoop:
    """Hunts for leads daily at 8am."""
    
    def __init__(self):
        self.hunt_time = time(8, 0)  # 8am
        self.last_hunt = None
    
    async def run(self):
        """Main loop execution."""
        logger.info("Lead Generation Loop started")
        
        while True:
            try:
                await self.check_schedule()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Lead Generation Loop error: {e}")
                await asyncio.sleep(60)
    
    async def check_schedule(self):
        """Check if it's time to hunt for leads."""
        now = datetime.now().time()
        today = datetime.now().date()
        
        if (now.hour == self.hunt_time.hour and 
            now.minute == self.hunt_time.minute and
            (self.last_hunt is None or self.last_hunt != today)):
            
            logger.info(f"Starting daily lead hunt at {self.hunt_time}")
            await self.hunt_leads()
            self.last_hunt = today
    
    async def hunt_leads(self):
        """Search for and score new leads."""
        # This would integrate with SerpAPI, Google Maps, etc.
        # Placeholder implementation
        logger.info("Lead hunting in progress...")
        
        # Mock lead data for demonstration
        mock_leads = [
            {
                "name": "ABC Plumbing Supply",
                "phone": "555-0100",
                "address": "123 Main St",
                "source": "google_maps",
                "business_type": "supplier"
            }
        ]
        
        with get_db() as db:
            for lead_data in mock_leads:
                # Check if lead already exists
                existing = db.query(Lead).filter(
                    Lead.phone == lead_data.get('phone')
                ).first()
                
                if not existing:
                    # Score the lead using AI
                    score = await self._score_lead(lead_data)
                    
                    # Generate opening line
                    opening_line = await self._generate_opening_line(lead_data)
                    
                    lead = Lead(
                        name=lead_data.get('name'),
                        phone=lead_data.get('phone'),
                        address=lead_data.get('address'),
                        source=lead_data.get('source'),
                        business_type=lead_data.get('business_type'),
                        score=score,
                        opening_line=opening_line
                    )
                    db.add(lead)
            
            db.commit()
        
        logger.info("Lead hunt completed")
    
    async def _score_lead(self, lead_data: dict) -> int:
        """Score a lead from 0-100 using AI."""
        prompt = f"""
        Score this potential customer lead from 0-100 based on relevance for a {settings.business_industry} business:
        
        Name: {lead_data.get('name')}
        Business Type: {lead_data.get('business_type')}
        Address: {lead_data.get('address')}
        
        Consider: property age, business type, location, and urgency signals.
        Return only a number between 0 and 100.
        """
        
        try:
            response = await ollama_client.generate(
                prompt=prompt,
                model=settings.ollama_reasoning_model,
                temperature=0.3
            )
            
            # Extract number from response
            digits = ''.join(filter(str.isdigit, response[:10]))
            if not digits:
                logger.warning(f"No score digits found in AI response: {response[:50]}")
                return 50  # Default score
            
            score = int(digits)
            return min(max(score, 0), 100)
        except (ValueError, Exception) as e:
            logger.error(f"Lead scoring error: {e}")
            return 50  # Default score
    
    async def _generate_opening_line(self, lead_data: dict) -> str:
        """Generate personalized opening line for lead outreach."""
        prompt = f"""
        Write a short, friendly opening line for a {settings.business_industry} business 
        reaching out to this potential customer:
        
        Name: {lead_data.get('name')}
        Business Type: {lead_data.get('business_type')}
        
        Keep it under 30 words and make it personalized.
        """
        
        try:
            opening = await ollama_client.generate(
                prompt=prompt,
                temperature=0.8
            )
            return opening.strip()
        except Exception as e:
            logger.error(f"Opening line generation error: {e}")
            return "Hi, I noticed your business and thought we might be able to help."
