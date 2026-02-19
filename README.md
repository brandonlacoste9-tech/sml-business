# 🐝 KimiClaw Business OS

**Your AI. Your data. Your business.**

KimiClaw is a self-hosted AI business operating system designed for small business owners in the trades and services industry — plumbers, electricians, cleaners, landscapers, HVAC technicians, and general contractors.

## What Is It?

KimiClaw functions as a fully autonomous AI employee that handles the administrative and growth side of a business around the clock, so the owner can focus entirely on doing the work.

### Core Features

- **AI Phone Receptionist** — Answers calls 24/7, books appointments, detects emergencies
- **Autonomous Lead Generation** — Finds and scores new leads every morning at 8am
- **Smart Calendar Management** — Auto-adjusts behavior based on capacity (Hunter/Surge modes)
- **Email Manager** — Drafts responses, sends follow-ups, handles booking confirmations
- **Automated Invoicing** — Generates invoices and tracks payments
- **WhatsApp Admin Control** — Manage your entire business from your phone
- **Photo Analysis** — Estimates job complexity and pricing from customer photos (Full Mode only)

## Quick Start

### One-Line Installation

```bash
curl -fsSL https://get.kimiclaw.com/install.sh | bash
```

The installer will:
1. Detect your OS and RAM
2. Install dependencies (Python, PostgreSQL, Redis, Ollama)
3. Download AI models
4. Run the 8-question setup wizard
5. Start the system as a background service

**Total setup time:** 20–45 minutes depending on internet speed

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kimiclaw.git
cd kimiclaw

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run setup wizard
python -m kimiclaw.cli.main install

# Start the server
python -m kimiclaw.cli.main serve
```

## System Requirements

### Minimum (Lite Mode)
- **RAM:** 8GB
- **Disk:** 20GB free space
- **OS:** Ubuntu 20.04+, macOS 11+, or Windows 10+ with WSL2
- **Features:** Voice, calendar, leads, email (no photo analysis)

### Recommended (Full Mode)
- **RAM:** 16GB
- **Disk:** 40GB free space
- **OS:** Ubuntu 20.04+, macOS 11+
- **Features:** All features including photo/vision AI

## CLI Commands

```bash
# View system status
kimiclaw status

# Run lead generation
kimiclaw leads

# Show configuration
kimiclaw config

# Start the server
kimiclaw serve

# Ask the AI a question
kimiclaw ask "What's on my calendar today?"

# Check installed models
kimiclaw models

# Run setup wizard
kimiclaw install
```

## Web Interfaces

- **Dashboard:** http://localhost:8000/dashboard
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## Architecture

### Technology Stack

- **Backend:** Python, FastAPI, asyncio
- **Database:** PostgreSQL (customer data, leads, history)
- **Cache:** Redis (customer memory, fast lookups)
- **AI:** Ollama (local AI runtime)
- **Integrations:** Twilio, Google Calendar/Gmail, SerpAPI, QuickBooks, Stripe

### AI Models (via Ollama)

| Task | Model | RAM Required |
|------|-------|--------------|
| Call handling / conversation | llama3.2 | ~3GB |
| Lead scoring / reasoning | mistral | ~5GB |
| Photo / job analysis | llava:13b | ~9GB |
| Customer memory search | nomic-embed-text | ~500MB |

### Autonomous Loops

Six loops run continuously in the background:

1. **Business Intelligence Loop** — Monitors metrics every 5 minutes, switches modes
2. **Communication Handler Loop** — Processes calls, SMS, emails every 30 seconds
3. **Advertising Loop** — Runs campaigns at configured times (9am, 3pm)
4. **Lead Generation Loop** — Daily hunt at 8am
5. **Financial Reconciliation Loop** — End-of-day reporting
6. **API Server** — FastAPI webhook receiver

## Configuration

Configuration is managed via environment variables in `.env`:

```bash
# Business Information
BUSINESS_NAME="Your Business Name"
BUSINESS_INDUSTRY="plumbing"
BUSINESS_LANGUAGE="en"  # en, fr, bilingual
BUSINESS_PHONE="+15555551234"
BUSINESS_WHATSAPP="+15555551234"

# Operating Hours
BUSINESS_HOURS_START="08:00"
BUSINESS_HOURS_END="17:00"
WEEKLY_CAPACITY=40

# Database
DATABASE_URL="postgresql://kimiclaw:password@localhost:5432/kimiclaw"
REDIS_URL="redis://localhost:6379/0"

# Ollama
OLLAMA_HOST="http://localhost:11434"

# External Services (Optional)
TWILIO_ACCOUNT_SID=""
TWILIO_AUTH_TOKEN=""
SERPAPI_KEY=""
GOOGLE_CREDENTIALS_PATH="credentials/google-credentials.json"
```

See `.env.example` for all configuration options.

## External Integrations

### Required for Full Functionality
- **Twilio** — Phone calls and SMS (required for voice features)
  - Sign up at https://www.twilio.com
  - ~$0.01/minute for calls, ~$0.0075/SMS

### Optional
- **SerpAPI** — Google Maps scraping for lead generation
  - Free tier: 100 searches/month
  - Sign up at https://serpapi.com
  
- **Google Calendar/Gmail** — Scheduling and email management
  - Enable Google Calendar API
  - Download credentials JSON
  
- **QuickBooks/Stripe** — Accounting and payments
  - Connect via OAuth

## Operating Modes

KimiClaw automatically adjusts its behavior based on calendar capacity:

- **Normal Mode** (60-90% capacity) — Standard operations
- **Hunter Mode** (<60% capacity) — Increases lead generation and ad frequency
- **Surge Mode** (>90% capacity) — Pauses low-value campaigns, suggests premium pricing

## Privacy & Security

- **All AI processing happens locally** via Ollama — no data sent to OpenAI or other cloud AI providers
- **Customer data never leaves your machine** — stored in local PostgreSQL database
- **No per-token API bills** — flat license fee with predictable costs
- **You own the system** — continues running even if KimiClaw company ceases operation

## Pricing

### SOLO — $99/month
- For single owner-operators
- 1 user, 1 calendar
- 50 calls/month, 20 leads/month
- Voice, calendar, basic leads, WhatsApp

### CREW — $299/month
- For teams of 3–10
- Unlimited calls, 100 leads/month
- Multi-calendar sync
- Full accounting integration
- Review requests, surge pricing

### ENTERPRISE — $999/month + setup fee
- Multi-location businesses
- Unlimited everything
- White-label branding
- Custom AI training
- API access

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=kimiclaw
```

### Project Structure

```
kimiclaw/
├── core/              # Core functionality
│   ├── config.py      # Configuration management
│   └── ollama_client.py  # Ollama AI client
├── modules/           # Autonomous loops
│   ├── business_intelligence.py
│   ├── communication_handler.py
│   └── lead_generation.py
├── models/            # Database models
│   └── database.py
├── integrations/      # External service integrations
├── cli/               # CLI interface
│   └── main.py
└── main.py           # FastAPI application
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

- **Documentation:** https://docs.kimiclaw.com
- **Issues:** https://github.com/yourusername/kimiclaw/issues
- **Email:** support@kimiclaw.com

---

**🐝 Built for trades. Proven in Montreal.**
