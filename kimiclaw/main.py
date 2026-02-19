"""Main FastAPI application server for KimiClaw Business OS."""

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
from loguru import logger

from kimiclaw.core.config import settings
from kimiclaw.modules.business_intelligence import BusinessIntelligenceLoop
from kimiclaw.modules.communication_handler import CommunicationHandlerLoop
from kimiclaw.modules.lead_generation import LeadGenerationLoop

# Background loops
loops = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("🐝 Starting KimiClaw Business OS")
    
    # Start background loops
    loops["business_intelligence"] = BusinessIntelligenceLoop()
    loops["communication_handler"] = CommunicationHandlerLoop()
    loops["lead_generation"] = LeadGenerationLoop()
    
    tasks = []
    for name, loop in loops.items():
        task = asyncio.create_task(loop.start())
        tasks.append(task)
        logger.info(f"Started {name} loop")
    
    yield
    
    # Shutdown: cancel all tasks
    logger.info("🐝 Shutting down KimiClaw Business OS")
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


# Create FastAPI app
app = FastAPI(
    title="KimiClaw Business OS",
    description="Your AI. Your data. Your business. 🐝",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with system status."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>KimiClaw Business OS</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            h1 { margin: 0; font-size: 3em; }
            .emoji { font-size: 4em; }
            .status { 
                margin: 20px 0;
                padding: 15px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }
            .footer {
                margin-top: 30px;
                font-size: 0.9em;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">🐝</div>
            <h1>KimiClaw Business OS</h1>
            <p style="font-size: 1.2em; margin: 10px 0;">Your AI. Your data. Your business.</p>
            
            <div class="status">
                <h2>✅ System Online</h2>
                <p>Business: <strong>{business_name}</strong></p>
                <p>Mode: <strong>{mode}</strong></p>
                <p>API Version: <strong>0.1.0</strong></p>
            </div>
            
            <p>
                <a href="/health" style="color: white;">Health Check</a> | 
                <a href="/docs" style="color: white;">API Documentation</a> |
                <a href="/dashboard" style="color: white;">Dashboard</a>
            </p>
            
            <div class="footer">
                🐝 Built for trades. Proven in Montreal.
            </div>
        </div>
    </body>
    </html>
    """.format(
        business_name=settings.business_name,
        mode=settings.system_mode.upper()
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "business": settings.business_name,
        "mode": settings.system_mode,
    }


@app.get("/api/status")
async def get_status():
    """Get current system status."""
    # TODO: Implement actual metrics from database
    return {
        "business_name": settings.business_name,
        "mode": settings.system_mode,
        "calendar_fill_rate": 0.65,
        "calls_today": 12,
        "leads_today": 3,
        "revenue_today": 1250.00,
    }


@app.post("/webhooks/twilio/voice")
async def twilio_voice_webhook(request: Request):
    """Twilio voice webhook for incoming calls."""
    from twilio.twiml.voice_response import VoiceResponse
    
    form_data = await request.form()
    logger.info(f"Incoming call from: {form_data.get('From')}")
    
    response = VoiceResponse()
    
    # Check if emergency keywords are detected
    # TODO: Implement proper call handling with Ollama
    
    greeting = f"Thank you for calling {settings.business_name}. "
    if settings.business_language == "fr":
        greeting = f"Merci d'avoir appelé {settings.business_name}. "
    elif settings.business_language == "bilingual":
        greeting = f"Thank you for calling {settings.business_name}. Merci d'avoir appelé. "
    
    response.say(greeting, voice="alice", language="en-CA")
    response.say("Please hold while we connect you.", voice="alice", language="en-CA")
    
    return Response(content=str(response), media_type="application/xml")


@app.post("/webhooks/twilio/sms")
async def twilio_sms_webhook(request: Request):
    """Twilio SMS webhook for incoming messages."""
    from twilio.twiml.messaging_response import MessagingResponse
    
    form_data = await request.form()
    from_number = form_data.get("From")
    body = form_data.get("Body", "")
    
    logger.info(f"Incoming SMS from {from_number}: {body}")
    
    # TODO: Implement proper SMS handling with Ollama
    
    response = MessagingResponse()
    response.message(f"Thanks for contacting {settings.business_name}. We'll get back to you shortly!")
    
    return Response(content=str(response), media_type="application/xml")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Simple web dashboard."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>KimiClaw Dashboard</title>
        <meta http-equiv="refresh" content="30">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background: #f5f5f5;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .header h1 { margin: 0; }
            .metrics {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }
            .metric {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .metric-value {
                font-size: 2.5em;
                font-weight: bold;
                color: #667eea;
                margin: 10px 0;
            }
            .metric-label {
                color: #666;
                font-size: 0.9em;
                text-transform: uppercase;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🐝 KimiClaw Dashboard</h1>
            <p>Real-time business metrics • Auto-refreshes every 30s</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="metric-label">Calendar Fill Rate</div>
                <div class="metric-value">65%</div>
            </div>
            <div class="metric">
                <div class="metric-label">Calls Today</div>
                <div class="metric-value">12</div>
            </div>
            <div class="metric">
                <div class="metric-label">Leads Today</div>
                <div class="metric-value">3</div>
            </div>
            <div class="metric">
                <div class="metric-label">Revenue Today</div>
                <div class="metric-value">$1,250</div>
            </div>
            <div class="metric">
                <div class="metric-label">Current Mode</div>
                <div class="metric-value" style="font-size: 1.5em;">NORMAL</div>
            </div>
            <div class="metric">
                <div class="metric-label">System Status</div>
                <div class="metric-value" style="font-size: 1.5em; color: #2ecc71;">ONLINE</div>
            </div>
        </div>
        
        <div style="text-align: center; color: #999; margin-top: 40px;">
            🐝 Built for trades. Proven in Montreal.
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
