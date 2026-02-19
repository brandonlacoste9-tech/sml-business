"""Business Intelligence Loop - Monitors business health and triggers mode changes."""
import asyncio
import logging
from datetime import datetime, timedelta
from kimiclaw.core.database import get_db
from kimiclaw.models.database import BusinessMetrics, Job
from kimiclaw.core.config import settings
from sqlalchemy import func

logger = logging.getLogger(__name__)


class BusinessIntelligenceLoop:
    """Monitors business health metrics every 5 minutes."""
    
    def __init__(self):
        self.interval = 300  # 5 minutes
        self.current_mode = "normal"
    
    async def run(self):
        """Main loop execution."""
        logger.info("Business Intelligence Loop started")
        
        while True:
            try:
                await self.check_health()
                await asyncio.sleep(self.interval)
            except Exception as e:
                logger.error(f"Business Intelligence Loop error: {e}")
                await asyncio.sleep(self.interval)
    
    async def check_health(self):
        """Check business health metrics and adjust mode."""
        with get_db() as db:
            # Get today's date range
            today = datetime.utcnow().date()
            tomorrow = today + timedelta(days=1)
            
            # Count scheduled jobs for next 7 days
            next_week = today + timedelta(days=7)
            total_capacity = settings.business_capacity * 7
            
            scheduled_jobs = db.query(func.count(Job.id)).filter(
                Job.status == "scheduled",
                Job.scheduled_start >= datetime.combine(today, datetime.min.time()),
                Job.scheduled_start < datetime.combine(next_week, datetime.max.time())
            ).scalar()
            
            # Calculate fill rate
            fill_rate = (scheduled_jobs / total_capacity * 100) if total_capacity > 0 else 0
            
            # Determine business mode
            new_mode = self._determine_mode(fill_rate)
            
            if new_mode != self.current_mode:
                logger.info(f"Business mode changed: {self.current_mode} -> {new_mode}")
                self.current_mode = new_mode
            
            # Update or create today's metrics
            metrics = db.query(BusinessMetrics).filter(
                func.date(BusinessMetrics.date) == today
            ).first()
            
            if not metrics:
                metrics = BusinessMetrics(date=datetime.utcnow())
                db.add(metrics)
            
            metrics.calendar_fill_rate = fill_rate
            metrics.jobs_scheduled = scheduled_jobs
            metrics.business_mode = self.current_mode
            
            db.commit()
            
            logger.debug(f"Health check: fill_rate={fill_rate:.1f}%, mode={self.current_mode}")
    
    def _determine_mode(self, fill_rate: float) -> str:
        """Determine business mode based on calendar fill rate."""
        if fill_rate < 60:
            return "hunter"  # Need more bookings
        elif fill_rate > 90:
            return "surge"   # Near capacity, increase prices
        else:
            return "normal"  # Operating normally
