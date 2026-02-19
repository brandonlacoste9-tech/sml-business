"""FastAPI server for webhooks and API endpoints."""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from kimiclaw.core.config import settings
from kimiclaw.core.database import get_db_session
from kimiclaw.models.database import Customer, Job, Lead, BusinessMetrics, Interaction
from kimiclaw.integrations.ollama_client import ollama_client
from sqlalchemy.orm import Session

# Version info
__version__ = "0.1.0"

app = FastAPI(
    title="KimiClaw Business OS API",
    description="API for KimiClaw Business Operating System",
    version=__version__
)

# CORS middleware - configured from environment
allowed_origins = ["*"] if settings.debug else []  # Restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class WebhookCall(BaseModel):
    from_number: str
    to_number: str
    call_sid: Optional[str] = None
    call_status: Optional[str] = None


class WebhookSMS(BaseModel):
    from_number: str
    to_number: str
    body: str
    message_sid: Optional[str] = None


class AdminCommand(BaseModel):
    command: str
    user_id: str


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    ollama_health = ollama_client.check_health()
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "business": settings.business_name,
        "ollama": ollama_health
    }


# Twilio webhooks
@app.post("/webhooks/twilio/voice")
async def twilio_voice_webhook(call: WebhookCall, db: Session = Depends(get_db_session)):
    """Handle incoming voice calls from Twilio."""
    # Find or create customer
    customer = db.query(Customer).filter(Customer.phone == call.from_number).first()
    if not customer:
        customer = Customer(name="Unknown", phone=call.from_number)
        db.add(customer)
        db.commit()
    
    # Log interaction
    interaction = Interaction(
        customer_id=customer.id,
        type="call",
        direction="inbound"
    )
    db.add(interaction)
    db.commit()
    
    return {
        "message": "Call received",
        "customer_id": customer.id
    }


@app.post("/webhooks/twilio/sms")
async def twilio_sms_webhook(sms: WebhookSMS, db: Session = Depends(get_db_session)):
    """Handle incoming SMS from Twilio."""
    # Find or create customer
    customer = db.query(Customer).filter(Customer.phone == sms.from_number).first()
    if not customer:
        customer = Customer(name="Unknown", phone=sms.from_number)
        db.add(customer)
        db.commit()
    
    # Log interaction
    interaction = Interaction(
        customer_id=customer.id,
        type="sms",
        direction="inbound",
        content=sms.body
    )
    db.add(interaction)
    db.commit()
    
    # Generate AI response
    response = await ollama_client.chat(
        messages=[{"role": "user", "content": sms.body}],
        system_prompt=f"You are an AI assistant for {settings.business_name}, a {settings.business_industry} business."
    )
    
    interaction.ai_response = response
    db.commit()
    
    return {
        "message": "SMS received",
        "response": response
    }


# Admin API
@app.post("/admin/command")
async def admin_command(cmd: AdminCommand, db: Session = Depends(get_db_session)):
    """Handle admin commands from WhatsApp."""
    command = cmd.command.lower().strip()
    
    if command == "status":
        # Get current metrics
        metrics = db.query(BusinessMetrics).order_by(
            BusinessMetrics.date.desc()
        ).first()
        
        if metrics:
            return {
                "command": "status",
                "fill_rate": metrics.calendar_fill_rate,
                "mode": metrics.business_mode,
                "jobs_today": metrics.jobs_completed,
                "revenue": metrics.revenue_today
            }
        else:
            return {"command": "status", "message": "No metrics available"}
    
    elif command == "leads":
        # Get hot leads (score >= 70)
        hot_leads = db.query(Lead).filter(
            Lead.score >= 70,
            Lead.status == "new"
        ).order_by(Lead.score.desc()).limit(5).all()
        
        return {
            "command": "leads",
            "count": len(hot_leads),
            "leads": [
                {
                    "name": lead.name,
                    "score": lead.score,
                    "opening_line": lead.opening_line
                }
                for lead in hot_leads
            ]
        }
    
    elif command in ["boost", "pause"]:
        return {
            "command": command,
            "message": f"{command.capitalize()} command received"
        }
    
    else:
        raise HTTPException(status_code=400, detail="Unknown command")


# Business data endpoints
@app.get("/api/customers")
async def get_customers(db: Session = Depends(get_db_session)):
    """Get all customers."""
    customers = db.query(Customer).all()
    return {"customers": customers}


@app.get("/api/jobs")
async def get_jobs(status: Optional[str] = None, db: Session = Depends(get_db_session)):
    """Get jobs, optionally filtered by status."""
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    jobs = query.all()
    return {"jobs": jobs}


@app.get("/api/leads")
async def get_leads(min_score: int = 0, db: Session = Depends(get_db_session)):
    """Get leads with minimum score."""
    leads = db.query(Lead).filter(Lead.score >= min_score).all()
    return {"leads": leads}


def create_app() -> FastAPI:
    """Create and configure FastAPI app."""
    return app
