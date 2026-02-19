#!/usr/bin/env python3
"""Main entry point for KimiClaw Business OS."""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from kimiclaw.cli.main import cli
    cli()
