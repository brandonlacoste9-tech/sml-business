#!/usr/bin/env python3
"""Simple script to run KimiClaw API server for development."""
import uvicorn
from kimiclaw.api.server import app
from kimiclaw.core.config import settings

if __name__ == "__main__":
    print(f"🐝 Starting KimiClaw API Server")
    print(f"Business: {settings.business_name}")
    print(f"Port: {settings.api_port}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.api_port,
        log_level=settings.log_level.lower()
    )
