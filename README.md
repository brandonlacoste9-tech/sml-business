# KimiClaw Business OS 🐝

**Your AI. Your data. Your business.**

KimiClaw is a self-hosted AI business operating system designed for small business owners in the trades and services industry. It functions as a fully autonomous AI employee that handles administrative tasks, customer communication, lead generation, and business operations 24/7.

## Features

- **AI Phone Receptionist** - Answers calls, books appointments, handles emergencies
- **Autonomous Lead Generation** - Finds and scores new customers daily
- **Smart Calendar Management** - Optimizes scheduling and capacity
- **Email Manager** - Handles inbox, sends follow-ups, confirms bookings
- **Automated Invoicing** - Generates invoices and tracks payments
- **WhatsApp Admin Control** - Control your business from your phone
- **Photo Analysis** - AI analyzes job photos for estimates (Full Mode)

## Quick Start

Install KimiClaw with a single command:

```bash
curl -fsSL https://get.kimiclaw.com/install.sh | bash
```

Answer 8 questions about your business, and within 30 minutes you'll have a working AI business assistant.

## Requirements

- **Lite Mode**: 8GB RAM (voice, calendar, basic features)
- **Full Mode**: 16GB+ RAM (includes photo analysis)
- Linux/macOS/Windows (via WSL2)
- PostgreSQL 12+
- Redis 6+

## Documentation

See the [docs](./docs) folder for detailed documentation:

- [Installation Guide](./docs/installation.md)
- [Configuration](./docs/configuration.md)
- [CLI Usage](./docs/cli-usage.md)
- [API Reference](./docs/api-reference.md)

## Pricing Tiers

- **SOLO** - $99/month - Single owner-operators
- **CREW** - $299/month - Teams of 3-10
- **ENTERPRISE** - $999/month - Multi-location businesses

## Architecture

Built with Python and FastAPI, KimiClaw runs six autonomous loops:

1. **Business Intelligence Loop** - Monitors health metrics
2. **Communication Handler Loop** - Processes calls, SMS, emails
3. **Advertising Loop** - Runs campaigns automatically
4. **Lead Generation Loop** - Daily lead hunting
5. **Financial Reconciliation Loop** - End-of-day reporting
6. **API Server** - Webhooks for Twilio, Google, admin commands

All AI runs locally via [Ollama](https://ollama.ai) - no data leaves your machine.

## Development

```bash
# Clone the repository
git clone https://github.com/brandonlacoste9-tech/sml-business.git
cd sml-business

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the application
python -m kimiclaw.main
```

## License

See [LICENSE](./LICENSE) for details.

## Support

- Documentation: [docs](./docs)
- Issues: [GitHub Issues](https://github.com/brandonlacoste9-tech/sml-business/issues)
- Email: hello@kimiclaw.com

---

*🐝 Built for trades. Proven in Montreal.*
# 🐝 KimiClaw Business OS — Self-Hosted

**AI Employee as a Service. On your machine.**

> Answers your calls. Books your jobs. Finds leads. Sends daily reports to your WhatsApp.
> 100% local AI via Ollama — no OpenAI bills, no cloud, no data leaks.

---

## ⚡ QUICK START

```bash
# One command install
curl -fsSL https://get.kimiclaw.com/install.sh | bash

# Start
sudo systemctl start kimiclaw

# Dashboard
open http://localhost:3000
```

**That's it.** Full onboarding: see [docs/ONBOARDING_GUIDE.md](docs/ONBOARDING_GUIDE.md)

---

## 🤖 AI MODELS (All Local)

| Task | Model | Size |
|------|-------|------|
| Answering calls | llama3.2 | 2GB |
| Lead scoring | mistral | 4GB |
| Photo analysis | llava:13b | 8GB |
| Memory search | nomic-embed-text | 300MB |

**Minimum RAM:** 8GB (lite) · **Recommended:** 16GB (full)

---

## 📦 WHAT'S INCLUDED

```
📞 AI Phone Receptionist     — Answers calls, books jobs 24/7
📅 Smart Calendar            — Auto-schedules around your capacity  
🎯 Lead Finder               — Hunts new customers every morning
📧 Email Manager             — Reads, drafts, sends replies
📊 Daily Reports             — WhatsApp summary every evening
⚡ Emergency Detection       — Escalates urgent calls instantly
🔄 Auto Mode Switching       — Hunter / Normal / Surge pricing
```

---

## 💬 WHATSAPP CONTROL

Text your AI from anywhere:

```
status  → Current stats
boost   → More aggressive outreach today
leads   → Today's hot leads
pause   → Stop all outbound activity
```

---

## 🏭 INDUSTRIES SUPPORTED

Plumbing · Electrical · Cleaning · HVAC · Landscaping · General Contractor

---

## 📋 SYSTEM REQUIREMENTS

| | Minimum | Recommended |
|-|---------|-------------|
| RAM | 8GB | 16GB |
| Storage | 20GB | 60GB SSD |
| OS | Ubuntu 20.04 / macOS 12 / WSL2 | Ubuntu 22.04 LTS |
| Python | 3.9 | 3.11 |

---

## 📖 DOCUMENTATION

- [Full Onboarding Guide](docs/ONBOARDING_GUIDE.md)
- [Configuration Reference](docs/CONFIG.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [API Reference](docs/API.md)

---

*🐝 KimiClaw — Built for trades. Proven in Montreal.*
*Your AI. Your data. Your business.*
