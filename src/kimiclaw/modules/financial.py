"""Financial Reconciliation Loop - End-of-day reporting and invoice generation."""
import asyncio
import logging
from datetime import datetime, time, timedelta
from kimiclaw.core.database import get_db
from kimiclaw.models.database import Invoice, Job, BusinessMetrics
from sqlalchemy import func

logger = logging.getLogger(__name__)


class FinancialReconciliationLoop:
    """Performs end-of-day financial reconciliation at 11pm."""
    
    def __init__(self):
        self.reconciliation_time = time(23, 0)  # 11pm
        self.last_reconciliation = None
    
    async def run(self):
        """Main loop execution."""
        logger.info("Financial Reconciliation Loop started")
        
        while True:
            try:
                await self.check_schedule()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Financial Reconciliation Loop error: {e}")
                await asyncio.sleep(60)
    
    async def check_schedule(self):
        """Check if it's time for end-of-day reconciliation."""
        now = datetime.now().time()
        today = datetime.now().date()
        
        if (now.hour == self.reconciliation_time.hour and 
            now.minute == self.reconciliation_time.minute and
            (self.last_reconciliation is None or self.last_reconciliation != today)):
            
            logger.info(f"Starting end-of-day reconciliation at {self.reconciliation_time}")
            await self.reconcile()
            self.last_reconciliation = today
    
    async def reconcile(self):
        """Perform end-of-day financial reconciliation."""
        with get_db() as db:
            today = datetime.utcnow().date()
            today_start = datetime.combine(today, datetime.min.time())
            today_end = datetime.combine(today, datetime.max.time())
            
            # Get completed jobs today
            completed_jobs = db.query(Job).filter(
                Job.status == "completed",
                Job.actual_end >= today_start,
                Job.actual_end <= today_end
            ).all()
            
            # Generate invoices for completed jobs without invoices
            for job in completed_jobs:
                existing_invoice = db.query(Invoice).filter(
                    Invoice.job_id == job.id
                ).first()
                
                if not existing_invoice and job.actual_price:
                    invoice = Invoice(
                        job_id=job.id,
                        invoice_number=f"INV-{datetime.now().strftime('%Y%m%d')}-{job.id}",
                        amount=job.actual_price,
                        tax_amount=job.actual_price * 0.15,  # 15% tax
                        total_amount=job.actual_price * 1.15,
                        due_date=datetime.utcnow() + timedelta(days=30)
                    )
                    db.add(invoice)
            
            # Calculate today's revenue
            paid_invoices = db.query(Invoice).join(Job).filter(
                Invoice.status == "paid",
                Invoice.paid_at >= today_start,
                Invoice.paid_at <= today_end
            ).all()
            
            revenue_today = sum(inv.total_amount for inv in paid_invoices)
            
            # Update metrics
            metrics = db.query(BusinessMetrics).filter(
                func.date(BusinessMetrics.date) == today
            ).first()
            
            if metrics:
                metrics.revenue_today = revenue_today
                metrics.jobs_completed = len(completed_jobs)
            
            db.commit()
            
            logger.info(f"Reconciliation complete: {len(completed_jobs)} jobs, ${revenue_today:.2f} revenue")
