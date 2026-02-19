#!/usr/bin/env python3
"""Database migration and management script."""

import sys
from loguru import logger
from kimiclaw.utils.database import init_db, drop_db, get_db
from kimiclaw.models.database import SystemConfig


def init():
    """Initialize database tables."""
    logger.info("Initializing database...")
    init_db()
    logger.info("✅ Database initialized successfully")


def reset():
    """Reset database (drop and recreate all tables)."""
    response = input("⚠️  This will DELETE ALL DATA. Are you sure? (type 'yes'): ")
    if response.lower() == 'yes':
        logger.warning("Dropping database...")
        drop_db()
        logger.info("Recreating database...")
        init_db()
        logger.info("✅ Database reset complete")
    else:
        logger.info("Operation cancelled")


def seed():
    """Seed database with initial data."""
    logger.info("Seeding database...")
    
    with get_db() as db:
        # Add default system config
        configs = [
            SystemConfig(key="system_initialized", value="true", value_type="bool"),
            SystemConfig(key="last_lead_hunt", value="", value_type="string"),
            SystemConfig(key="current_mode", value="normal", value_type="string"),
        ]
        
        for config in configs:
            existing = db.query(SystemConfig).filter_by(key=config.key).first()
            if not existing:
                db.add(config)
        
        db.commit()
    
    logger.info("✅ Database seeded successfully")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python migrate.py [init|reset|seed]")
        print("  init  - Initialize database tables")
        print("  reset - Drop and recreate all tables (WARNING: deletes all data)")
        print("  seed  - Seed database with initial data")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init()
    elif command == "reset":
        reset()
    elif command == "seed":
        seed()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
