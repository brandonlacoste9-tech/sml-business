"""CLI interface for KimiClaw Business OS."""
import asyncio
import sys
import argparse
from datetime import datetime
from kimiclaw.core.config import settings
from kimiclaw.core.database import get_db, init_db
from kimiclaw.models.database import BusinessMetrics, Lead, Job, Customer
from kimiclaw.integrations.ollama_client import ollama_client
from kimiclaw.modules.lead_generation import LeadGenerationLoop
from sqlalchemy import func


def status():
    """Show current business status."""
    with get_db() as db:
        # Get latest metrics
        metrics = db.query(BusinessMetrics).order_by(
            BusinessMetrics.date.desc()
        ).first()
        
        if not metrics:
            print("No metrics available yet. System may still be initializing.")
            return
        
        print("\n🐝 KimiClaw Business OS Status")
        print("=" * 50)
        print(f"Business: {settings.business_name}")
        print(f"Industry: {settings.business_industry}")
        print(f"Mode: {metrics.business_mode.upper()}")
        print(f"\nCalendar Fill Rate: {metrics.calendar_fill_rate:.1f}%")
        print(f"Jobs Scheduled: {metrics.jobs_scheduled}")
        print(f"Jobs Completed Today: {metrics.jobs_completed}")
        print(f"\nLeads Generated: {metrics.leads_generated}")
        print(f"Leads Converted: {metrics.leads_converted}")
        print(f"\nCalls Answered: {metrics.calls_answered}/{metrics.calls_received}")
        print(f"Revenue Today: ${metrics.revenue_today:.2f}")
        print(f"Revenue Pending: ${metrics.revenue_pending:.2f}")
        print("=" * 50)


def leads_hunt():
    """Manually trigger lead hunting."""
    print("🔍 Starting manual lead hunt...")
    loop = LeadGenerationLoop()
    asyncio.run(loop.hunt_leads())
    print("✓ Lead hunt completed")


def leads_list(min_score: int = 0):
    """List leads with optional minimum score."""
    with get_db() as db:
        leads = db.query(Lead).filter(
            Lead.score >= min_score
        ).order_by(Lead.score.desc()).all()
        
        if not leads:
            print(f"No leads found with score >= {min_score}")
            return
        
        print(f"\n🎯 Leads (score >= {min_score})")
        print("=" * 80)
        
        for lead in leads:
            print(f"\nName: {lead.name}")
            print(f"Score: {lead.score}/100")
            print(f"Phone: {lead.phone or 'N/A'}")
            print(f"Source: {lead.source}")
            print(f"Status: {lead.status}")
            if lead.opening_line:
                print(f"Opening: {lead.opening_line}")
            print("-" * 80)


def jobs_list(status_filter: str = None):
    """List jobs, optionally filtered by status."""
    with get_db() as db:
        query = db.query(Job)
        if status_filter:
            query = query.filter(Job.status == status_filter)
        
        jobs = query.order_by(Job.scheduled_start.desc()).all()
        
        if not jobs:
            print(f"No jobs found" + (f" with status '{status_filter}'" if status_filter else ""))
            return
        
        print(f"\n📋 Jobs" + (f" ({status_filter})" if status_filter else ""))
        print("=" * 80)
        
        for job in jobs:
            customer = db.query(Customer).filter(Customer.id == job.customer_id).first()
            print(f"\nJob #{job.id}: {job.title}")
            print(f"Customer: {customer.name if customer else 'Unknown'}")
            print(f"Status: {job.status}")
            print(f"Scheduled: {job.scheduled_start.strftime('%Y-%m-%d %H:%M') if job.scheduled_start else 'Not scheduled'}")
            if job.estimated_price:
                print(f"Price: ${job.estimated_price:.2f}")
            print("-" * 80)


def health():
    """Check system health."""
    print("\n🏥 System Health Check")
    print("=" * 50)
    
    # Check Ollama
    ollama_health = ollama_client.check_health()
    print(f"\nOllama: {ollama_health['status']}")
    if ollama_health['status'] == 'healthy':
        print(f"Host: {ollama_health['host']}")
        print(f"Models: {', '.join(ollama_health['models'])}")
    else:
        print(f"Error: {ollama_health.get('error', 'Unknown')}")
    
    # Check database
    try:
        with get_db() as db:
            count = db.query(func.count(Customer.id)).scalar()
            print(f"\nDatabase: healthy")
            print(f"Customers: {count}")
    except Exception as e:
        print(f"\nDatabase: unhealthy")
        print(f"Error: {e}")
    
    print("=" * 50)


def init():
    """Initialize database."""
    print("Initializing database...")
    init_db()
    print("✓ Database initialized")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="KimiClaw Business OS CLI",
        prog="kimiclaw"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    subparsers.add_parser("status", help="Show business status")
    
    # Leads commands
    leads_parser = subparsers.add_parser("leads", help="Manage leads")
    leads_subparsers = leads_parser.add_subparsers(dest="leads_command")
    leads_subparsers.add_parser("hunt", help="Hunt for new leads")
    list_parser = leads_subparsers.add_parser("list", help="List leads")
    list_parser.add_argument("--min-score", type=int, default=0, help="Minimum score")
    
    # Jobs command
    jobs_parser = subparsers.add_parser("jobs", help="List jobs")
    jobs_parser.add_argument("--status", type=str, help="Filter by status")
    
    # Health command
    subparsers.add_parser("health", help="Check system health")
    
    # Init command
    subparsers.add_parser("init", help="Initialize database")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    if args.command == "status":
        status()
    elif args.command == "leads":
        if args.leads_command == "hunt":
            leads_hunt()
        elif args.leads_command == "list":
            leads_list(args.min_score)
        else:
            leads_parser.print_help()
    elif args.command == "jobs":
        jobs_list(args.status)
    elif args.command == "health":
        health()
    elif args.command == "init":
        init()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
