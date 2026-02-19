"""Database models for KimiClaw Business OS"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Customer(Base):
    """Customer information and interaction history."""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    
    # Customer metadata
    language_preference = Column(String, default="en")
    lifetime_value = Column(Float, default=0.0)
    total_jobs = Column(Integer, default=0)
    
    # Preferences and notes
    preferences = Column(JSON, default={})
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    jobs = relationship("Job", back_populates="customer")
    interactions = relationship("Interaction", back_populates="customer")


class Lead(Base):
    """Potential customers from lead generation."""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    
    # Lead information
    source = Column(String, nullable=False)  # google_maps, directory, classified, referral
    business_type = Column(String, nullable=True)
    property_age = Column(Integer, nullable=True)
    
    # Scoring
    score = Column(Integer, default=0)  # 0-100
    urgency_signals = Column(JSON, default=[])
    
    # Status
    status = Column(String, default="new")  # new, contacted, qualified, converted, rejected
    contacted_at = Column(DateTime, nullable=True)
    converted_at = Column(DateTime, nullable=True)
    
    # AI-generated opening line
    opening_line = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Job(Base):
    """Jobs/appointments for customers."""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    # Job details
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    service_type = Column(String, nullable=False)
    
    # Scheduling
    scheduled_start = Column(DateTime, nullable=True)
    scheduled_end = Column(DateTime, nullable=True)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    
    # Status
    status = Column(String, default="scheduled")  # scheduled, in_progress, completed, cancelled
    
    # Pricing
    estimated_price = Column(Float, nullable=True)
    actual_price = Column(Float, nullable=True)
    deposit_amount = Column(Float, default=0.0)
    deposit_paid = Column(Boolean, default=False)
    
    # Emergency flag
    is_emergency = Column(Boolean, default=False)
    
    # Photo analysis
    photo_urls = Column(JSON, default=[])
    photo_analysis = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="jobs")
    invoice = relationship("Invoice", back_populates="job", uselist=False)


class Interaction(Base):
    """Customer interactions (calls, emails, SMS)."""
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    
    # Interaction details
    type = Column(String, nullable=False)  # call, email, sms, whatsapp
    direction = Column(String, nullable=False)  # inbound, outbound
    
    # Content
    content = Column(Text, nullable=True)
    ai_response = Column(Text, nullable=True)
    
    # Metadata
    duration_seconds = Column(Integer, nullable=True)
    recording_url = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)  # positive, neutral, negative
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="interactions")


class Invoice(Base):
    """Invoices for completed jobs."""
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, unique=True)
    
    # Invoice details
    invoice_number = Column(String, unique=True, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    
    # Payment
    status = Column(String, default="pending")  # pending, paid, overdue, cancelled
    payment_method = Column(String, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Due date
    due_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="invoice")


class BusinessMetrics(Base):
    """Daily business health metrics."""
    __tablename__ = "business_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    
    # Calendar metrics
    calendar_fill_rate = Column(Float, default=0.0)  # 0-100%
    jobs_scheduled = Column(Integer, default=0)
    jobs_completed = Column(Integer, default=0)
    jobs_cancelled = Column(Integer, default=0)
    
    # Lead metrics
    leads_generated = Column(Integer, default=0)
    leads_contacted = Column(Integer, default=0)
    leads_converted = Column(Integer, default=0)
    
    # Communication metrics
    calls_received = Column(Integer, default=0)
    calls_answered = Column(Integer, default=0)
    calls_missed = Column(Integer, default=0)
    emails_received = Column(Integer, default=0)
    emails_sent = Column(Integer, default=0)
    
    # Financial metrics
    revenue_today = Column(Float, default=0.0)
    revenue_pending = Column(Float, default=0.0)
    
    # Mode
    business_mode = Column(String, default="normal")  # normal, hunter, surge
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
