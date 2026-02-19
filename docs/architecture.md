# KimiClaw Business OS - Technical Architecture

## Overview

KimiClaw is a self-hosted AI business operating system built with Python and FastAPI, designed specifically for trades and services businesses. It runs entirely on local infrastructure using Ollama for AI inference, ensuring data privacy and cost predictability.

## System Architecture

### Core Components

1. **Main Application** (`src/kimiclaw/main.py`)
   - Orchestrates all autonomous loops
   - Handles graceful startup/shutdown
   - Signal handling for clean termination

2. **Configuration Management** (`src/kimiclaw/core/config.py`)
   - Pydantic-based settings
   - Environment variable loading from `.env`
   - Type-safe configuration access

3. **Database Layer** (`src/kimiclaw/models/`)
   - SQLAlchemy ORM models
   - PostgreSQL for persistent storage
   - Redis for caching and fast lookups

4. **AI Integration** (`src/kimiclaw/integrations/ollama_client.py`)
   - Local AI inference via Ollama
   - Model routing for different tasks
   - Vision, conversation, reasoning, and embedding models

5. **API Server** (`src/kimiclaw/api/server.py`)
   - FastAPI REST API
   - Webhook endpoints for Twilio
   - Admin command interface
   - Business data endpoints

6. **CLI Interface** (`src/kimiclaw/cli.py`)
   - Command-line management tool
   - Status monitoring
   - Lead and job management
   - System health checks

### Autonomous Loops

KimiClaw runs six independent asynchronous loops:

#### 1. Business Intelligence Loop
- **Interval:** Every 5 minutes
- **Purpose:** Monitor business health metrics
- **Actions:**
  - Calculate calendar fill rate
  - Determine business mode (normal/hunter/surge)
  - Update daily metrics
  - Trigger mode-based behaviors

#### 2. Communication Handler Loop
- **Interval:** Every 30 seconds
- **Purpose:** Process inbound communications
- **Actions:**
  - Handle phone calls via Twilio
  - Process SMS messages
  - Manage email inbox
  - Generate AI responses
  - Log all interactions

#### 3. Advertising Loop
- **Schedule:** 9am and 3pm daily
- **Purpose:** Run marketing campaigns
- **Actions:**
  - Execute scheduled campaigns
  - Adjust based on business mode
  - Track campaign performance

#### 4. Lead Generation Loop
- **Schedule:** 8am daily
- **Purpose:** Hunt for new customers
- **Actions:**
  - Search Google Maps, directories
  - Score leads 0-100 using AI
  - Generate personalized opening lines
  - Queue hot leads (70+) for outreach

#### 5. Financial Reconciliation Loop
- **Schedule:** 11pm daily (end-of-day)
- **Purpose:** Financial reporting and invoicing
- **Actions:**
  - Generate invoices for completed jobs
  - Calculate daily revenue
  - Update financial metrics
  - Prepare daily report

#### 6. API Server
- **Always running**
- **Purpose:** Receive webhooks and API requests
- **Endpoints:**
  - `/health` - System health check
  - `/webhooks/twilio/voice` - Voice call handling
  - `/webhooks/twilio/sms` - SMS handling
  - `/admin/command` - WhatsApp admin commands
  - `/api/customers` - Customer data
  - `/api/jobs` - Job data
  - `/api/leads` - Lead data

## Data Models

### Customer
- Basic information (name, phone, email, address)
- Language preference
- Lifetime value and total jobs
- Custom preferences and notes

### Lead
- Contact information
- Source (google_maps, directory, etc.)
- AI-calculated score (0-100)
- Urgency signals
- Status tracking (new, contacted, qualified, converted)
- Personalized opening line

### Job
- Customer reference
- Service type and description
- Scheduling (scheduled and actual times)
- Status (scheduled, in_progress, completed, cancelled)
- Pricing (estimated and actual)
- Emergency flag
- Photo URLs and AI analysis

### Interaction
- Customer reference
- Type (call, email, sms, whatsapp)
- Direction (inbound, outbound)
- Content and AI response
- Duration and recording URL
- Sentiment analysis

### Invoice
- Job reference
- Invoice number and amounts
- Payment status and method
- Due date tracking

### BusinessMetrics
- Daily snapshot of business health
- Calendar fill rate
- Job counts (scheduled, completed, cancelled)
- Lead metrics (generated, contacted, converted)
- Communication metrics (calls, emails)
- Financial metrics (revenue)
- Current business mode

## AI Model Strategy

### Model Selection by Task

| Task | Model | RAM Required | Purpose |
|------|-------|-------------|---------|
| Call handling | llama3.2 | ~3GB | Natural conversation |
| Lead scoring | mistral | ~5GB | Reasoning and analysis |
| Photo analysis | llava:13b | ~9GB | Vision and estimation |
| Embeddings | nomic-embed-text | ~500MB | Semantic search |

### Lite vs Full Mode

- **Lite Mode (8GB RAM):** Voice, calendar, leads, email - no photo analysis
- **Full Mode (16GB+ RAM):** All features including job photo analysis

## External Integrations

### Required for Full Functionality

1. **Twilio** - Voice calls and SMS
   - Call forwarding and answering
   - SMS communication
   - Emergency detection

2. **SerpAPI** - Lead generation
   - Google Maps scraping
   - Local business search
   - Directory listings

3. **Google Calendar** - Scheduling
   - Appointment booking
   - Calendar fill rate tracking
   - Availability management

4. **Gmail** - Email management
   - Inbox monitoring
   - Auto-response generation
   - Follow-up sequences

### Optional Integrations

1. **QuickBooks** - Accounting
2. **Stripe** - Payment processing
3. **WhatsApp Business API** - Admin control

## Deployment

### System Requirements

- **Minimum:** 8GB RAM, 2 CPU cores, 50GB storage
- **Recommended:** 16GB RAM, 4 CPU cores, 100GB storage
- **OS:** Linux (Ubuntu 20.04+), macOS 12+, or Windows with WSL2

### Installation

```bash
curl -fsSL https://get.kimiclaw.com/install.sh | bash
```

### Service Management

```bash
# Status
systemctl status kimiclaw

# Start/Stop/Restart
systemctl start kimiclaw
systemctl stop kimiclaw
systemctl restart kimiclaw

# Logs
journalctl -u kimiclaw -f
```

### CLI Commands

```bash
kimiclaw status          # Business status
kimiclaw leads hunt      # Manual lead hunt
kimiclaw leads list      # List leads
kimiclaw jobs --status   # List jobs by status
kimiclaw health          # System health check
kimiclaw init            # Initialize database
```

## Development

### Project Structure

```
sml-business/
├── src/kimiclaw/
│   ├── api/              # FastAPI server
│   ├── core/             # Core configuration and database
│   ├── integrations/     # External service clients
│   ├── models/           # Database models
│   ├── modules/          # Autonomous loops
│   ├── utils/            # Utility functions
│   ├── main.py           # Application entry point
│   └── cli.py            # CLI interface
├── tests/                # Test suite
├── scripts/              # Helper scripts
├── docs/                 # Documentation
├── requirements.txt      # Python dependencies
└── setup.py              # Package configuration
```

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
python -m kimiclaw.cli init

# Run the application
python -m kimiclaw.main

# Or run API server only
python scripts/run_api.py
```

### Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=kimiclaw --cov-report=html
```

## Security Considerations

1. **Local AI** - No data sent to external AI providers
2. **Database encryption** - Sensitive data at rest
3. **API authentication** - Webhook signature verification
4. **Secrets management** - Environment variables, not hardcoded
5. **Rate limiting** - Protection against abuse

## Scalability

- **Single business:** Designed for 1-10 employees
- **Multi-tenant:** Each business gets own database namespace
- **Horizontal scaling:** Multiple API servers behind load balancer
- **Database:** PostgreSQL read replicas for high-traffic scenarios

## Monitoring

1. **Health endpoint:** `/health` for uptime monitoring
2. **Metrics:** Daily BusinessMetrics snapshots
3. **Logging:** Structured logging to stdout/file
4. **Alerts:** Configurable alerts for critical events

## Future Enhancements

1. **WhatsApp Business API integration** for admin control
2. **Web dashboard** at port 3000 for visual management
3. **Mobile app** for on-the-go business monitoring
4. **Advanced analytics** with trend forecasting
5. **Multi-language support** beyond English/French
6. **Industry-specific templates** for different trades
7. **CRM features** for customer relationship management
8. **Automated review requests** after job completion

---

*For more information, see [Installation Guide](installation.md) and [API Reference](api-reference.md)*
