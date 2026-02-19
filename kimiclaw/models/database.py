"""Database models for KimiClaw Business OS."""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, Text, JSON, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Customer(Base):
    """Customer model."""
    
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    language = Column(String(2), default="en")  # en, fr
    
    # Customer value tracking
    lifetime_value = Column(Float, default=0.0)
    total_jobs = Column(Integer, default=0)
    
    # Preferences and notes
    preferences = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="customer")
    interactions = relationship("Interaction", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")


class Appointment(Base):
    """Appointment model."""
    
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    # Appointment details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    service_type = Column(String(100), nullable=True)
    
    # Scheduling
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(String(20), default="scheduled")  # scheduled, completed, cancelled, no_show
    
    # Pricing
    estimated_price = Column(Float, nullable=True)
    actual_price = Column(Float, nullable=True)
    
    # Emergency flag
    is_emergency = Column(Boolean, default=False)
    
    # External calendar sync
    google_event_id = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="appointments")


class Lead(Base):
    """Lead model."""
    
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True)
    
    # Lead information
    business_name = Column(String(255), nullable=True)
    contact_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    
    # Lead source and scoring
    source = Column(String(100), nullable=True)  # google_maps, directory, referral
    score = Column(Integer, default=0)  # 0-100
    status = Column(String(20), default="new")  # new, contacted, qualified, converted, lost
    
    # Lead details
    lead_type = Column(String(100), nullable=True)
    urgency = Column(String(20), nullable=True)  # low, medium, high, emergency
    notes = Column(Text, nullable=True)
    
    # AI-generated content
    opening_line = Column(Text, nullable=True)
    
    # Outreach tracking
    contacted_at = Column(DateTime, nullable=True)
    last_followup_at = Column(DateTime, nullable=True)
    converted_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Interaction(Base):
    """Customer interaction history."""
    
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    
    # Interaction details
    interaction_type = Column(String(50), nullable=False)  # call, sms, email, visit
    direction = Column(String(10), nullable=False)  # inbound, outbound
    
    # Content
    summary = Column(Text, nullable=True)
    transcript = Column(Text, nullable=True)
    sentiment = Column(String(20), nullable=True)  # positive, neutral, negative
    
    # Call-specific fields
    call_duration_seconds = Column(Integer, nullable=True)
    call_sid = Column(String(255), nullable=True)  # Twilio SID
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="interactions")


class Invoice(Base):
    """Invoice model."""
    
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    # Invoice details
    invoice_number = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Financial
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    
    # Status
    status = Column(String(20), default="draft")  # draft, sent, paid, overdue, cancelled
    
    # Payment tracking
    payment_method = Column(String(50), nullable=True)
    payment_reference = Column(String(255), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Dates
    issued_at = Column(DateTime, nullable=True)
    due_at = Column(DateTime, nullable=True)
    
    # External integrations
    quickbooks_id = Column(String(255), nullable=True)
    stripe_invoice_id = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="invoices")


class BusinessMetrics(Base):
    """Business health metrics snapshot."""
    
    __tablename__ = "business_metrics"
    
    id = Column(Integer, primary_key=True)
    
    # Calendar metrics
    calendar_fill_rate = Column(Float, default=0.0)  # 0.0 to 1.0
    upcoming_appointments = Column(Integer, default=0)
    
    # Revenue metrics
    revenue_today = Column(Float, default=0.0)
    revenue_week = Column(Float, default=0.0)
    revenue_month = Column(Float, default=0.0)
    
    # Lead metrics
    leads_today = Column(Integer, default=0)
    leads_week = Column(Integer, default=0)
    hot_leads_count = Column(Integer, default=0)
    
    # Communication metrics
    calls_answered = Column(Integer, default=0)
    calls_missed = Column(Integer, default=0)
    emails_sent = Column(Integer, default=0)
    
    # System mode
    current_mode = Column(String(20), default="normal")  # normal, hunter, surge
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)


class SystemConfig(Base):
    """System configuration key-value store."""
    
    __tablename__ = "system_config"
    
    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    value_type = Column(String(20), default="string")  # string, int, float, bool, json
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
