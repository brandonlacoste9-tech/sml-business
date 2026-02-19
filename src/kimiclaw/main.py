"""Main entry point for KimiClaw Business OS."""
import asyncio
import logging
import signal
from typing import List
from kimiclaw.core.config import settings
from kimiclaw.core.database import init_db
from kimiclaw.modules.business_intelligence import BusinessIntelligenceLoop
from kimiclaw.modules.communication_handler import CommunicationHandlerLoop
from kimiclaw.modules.advertising import AdvertisingLoop
from kimiclaw.modules.lead_generation import LeadGenerationLoop
from kimiclaw.modules.financial import FinancialReconciliationLoop
from kimiclaw.api.server import create_app

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KimiClawOS:
    """Main application orchestrator for KimiClaw Business OS."""
    
    def __init__(self):
        self.loops: List[asyncio.Task] = []
        self.running = False
        
        # Initialize autonomous loops
        self.business_intelligence = BusinessIntelligenceLoop()
        self.communication_handler = CommunicationHandlerLoop()
        self.advertising = AdvertisingLoop()
        self.lead_generation = LeadGenerationLoop()
        self.financial = FinancialReconciliationLoop()
        
    async def start(self):
        """Start all autonomous loops and API server."""
        logger.info("🐝 KimiClaw Business OS starting...")
        
        # Initialize database
        init_db()
        logger.info("Database initialized")
        
        # Start autonomous loops
        self.running = True
        self.loops = [
            asyncio.create_task(self.business_intelligence.run()),
            asyncio.create_task(self.communication_handler.run()),
            asyncio.create_task(self.advertising.run()),
            asyncio.create_task(self.lead_generation.run()),
            asyncio.create_task(self.financial.run()),
        ]
        
        logger.info("All autonomous loops started")
        logger.info(f"Business: {settings.business_name}")
        logger.info(f"Industry: {settings.business_industry}")
        logger.info(f"Language: {settings.business_language}")
        logger.info("🐝 KimiClaw Business OS is running!")
        
        # Keep running
        try:
            await asyncio.gather(*self.loops)
        except asyncio.CancelledError:
            logger.info("Loops cancelled")
    
    async def stop(self):
        """Stop all autonomous loops."""
        logger.info("🐝 KimiClaw Business OS shutting down...")
        self.running = False
        
        # Cancel all loops
        for loop in self.loops:
            loop.cancel()
        
        # Wait for all loops to finish
        await asyncio.gather(*self.loops, return_exceptions=True)
        
        logger.info("All loops stopped")
        logger.info("🐝 KimiClaw Business OS stopped")


async def main():
    """Main application entry point."""
    app = KimiClawOS()
    
    # Handle shutdown signals
    loop = asyncio.get_event_loop()
    
    def shutdown():
        asyncio.create_task(app.stop())
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown)
    
    try:
        await app.start()
    except KeyboardInterrupt:
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
