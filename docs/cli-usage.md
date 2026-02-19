# CLI Usage Guide

The `kimiclaw` command-line interface provides quick access to business operations and system management.

## Installation

After running the installation script, the CLI is available at:

```bash
kimiclaw [command] [options]
```

If the command is not found, add it to your PATH:

```bash
export PATH="$HOME/.kimiclaw/venv/bin:$PATH"
# Add to ~/.bashrc or ~/.zshrc to make permanent
```

## Commands

### Status

Get current business status and metrics.

```bash
kimiclaw status
```

**Output:**
```
🐝 KimiClaw Business OS Status
==================================================
Business: Montreal Plumbing Pros
Industry: plumbing
Mode: NORMAL

Calendar Fill Rate: 75.0%
Jobs Scheduled: 21
Jobs Completed Today: 3

Leads Generated: 15
Leads Converted: 2

Calls Answered: 18/20
Revenue Today: $2,450.00
Revenue Pending: $1,200.00
==================================================
```

### Leads

#### Hunt for New Leads

Manually trigger lead generation (normally runs at 8am daily).

```bash
kimiclaw leads hunt
```

**Output:**
```
🔍 Starting manual lead hunt...
✓ Lead hunt completed
```

#### List Leads

View leads with optional score filtering.

```bash
# List all leads
kimiclaw leads list

# List hot leads (score >= 70)
kimiclaw leads list --min-score 70

# List only qualified leads
kimiclaw leads list --min-score 80
```

**Output:**
```
🎯 Leads (score >= 70)
================================================================================

Name: ABC Property Management
Score: 85/100
Phone: +15145551234
Source: google_maps
Status: new
Opening: Hi ABC, noticed your portfolio includes buildings from the 1980s - 
         we specialize in preventive plumbing for older properties.
--------------------------------------------------------------------------------

Name: Downtown Condos Inc
Score: 78/100
Phone: +15145555678
Source: directory
Status: contacted
Opening: Hello, saw you manage 12 buildings downtown - we offer monthly 
         maintenance plans that reduce emergency calls by 60%.
--------------------------------------------------------------------------------
```

### Jobs

List jobs with optional status filtering.

```bash
# List all jobs
kimiclaw jobs

# List scheduled jobs
kimiclaw jobs --status scheduled

# List completed jobs
kimiclaw jobs --status completed

# List in-progress jobs
kimiclaw jobs --status in_progress
```

**Output:**
```
📋 Jobs (scheduled)
================================================================================

Job #42: Kitchen Sink Repair
Customer: John Smith
Status: scheduled
Scheduled: 2026-02-20 14:00
Price: $150.00
--------------------------------------------------------------------------------

Job #43: Water Heater Installation
Customer: Mary Johnson
Status: scheduled
Scheduled: 2026-02-21 09:00
Price: $1,200.00
--------------------------------------------------------------------------------
```

### Health Check

Verify system health and connectivity.

```bash
kimiclaw health
```

**Output:**
```
🏥 System Health Check
==================================================

Ollama: healthy
Host: http://localhost:11434
Models: llama3.2, mistral, llava:13b, nomic-embed-text

Database: healthy
Customers: 247

Redis: healthy
Cache: operational

==================================================
```

### Initialize Database

Set up database schema (run once during installation).

```bash
kimiclaw init
```

**Output:**
```
Initializing database...
✓ Database initialized
```

## Exit Codes

- `0` - Success
- `1` - General error
- `2` - Configuration error
- `3` - Database error
- `4` - External service error

## Common Workflows

### Morning Routine

```bash
# Check overnight status
kimiclaw status

# Review new leads
kimiclaw leads list --min-score 70

# Check today's jobs
kimiclaw jobs --status scheduled
```

### Lead Generation

```bash
# Manual hunt (if needed outside 8am schedule)
kimiclaw leads hunt

# Review and prioritize
kimiclaw leads list --min-score 80
```

### End of Day

```bash
# Check completion
kimiclaw jobs --status completed

# Review revenue
kimiclaw status
```

### Troubleshooting

```bash
# Check system health
kimiclaw health

# If issues, check logs
journalctl -u kimiclaw -n 100
```

## Advanced Usage

### With Environment Variables

```bash
# Use different environment file
ENV_FILE=/path/to/.env kimiclaw status
```

### Scripting

```bash
#!/bin/bash
# daily_report.sh - Generate daily business report

STATUS=$(kimiclaw status)
LEADS=$(kimiclaw leads list --min-score 70)

echo "$STATUS" | mail -s "Daily Report" owner@business.com
```

### JSON Output (Future)

```bash
# Planned for future release
kimiclaw status --json
kimiclaw leads list --json --min-score 70
```

## Getting Help

```bash
# General help
kimiclaw --help

# Command-specific help
kimiclaw leads --help
kimiclaw jobs --help
```

## Next Steps

- [Configuration Guide](configuration.md)
- [API Reference](api-reference.md)
- [Architecture Overview](architecture.md)
