# KimiClaw Business OS - Quick Start Guide

## Prerequisites

- Python 3.9 or higher
- PostgreSQL (or use Docker)
- Redis (or use Docker)
- Ollama (for local AI)

## 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/kimiclaw.git
cd kimiclaw

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## 2. Start Infrastructure

### Option A: Using Docker (Recommended)
```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Check services are running
docker-compose ps
```

### Option B: Local Installation
```bash
# On Ubuntu/Debian
sudo apt-get install postgresql redis-server

# On macOS
brew install postgresql redis

# Start services
sudo systemctl start postgresql redis-server  # Linux
brew services start postgresql redis  # macOS
```

## 3. Install Ollama

```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve  # Keep this running in a separate terminal

# Pull required models (in another terminal)
ollama pull llama3.2
ollama pull mistral
ollama pull nomic-embed-text

# Optional: For Full Mode (16GB+ RAM)
ollama pull llava:13b
```

## 4. Configure KimiClaw

```bash
# Run the interactive setup wizard
python -m kimiclaw.cli.main install
```

Or manually create `.env`:

```bash
cp .env.example .env
# Edit .env with your settings
```

**Minimal configuration:**
```env
BUSINESS_NAME="Your Business Name"
BUSINESS_INDUSTRY="plumbing"
BUSINESS_LANGUAGE="en"
BUSINESS_PHONE="+15555551234"
BUSINESS_WHATSAPP="+15555551234"

DATABASE_URL="postgresql://kimiclaw:kimiclaw@localhost:5432/kimiclaw"
REDIS_URL="redis://localhost:6379/0"
OLLAMA_HOST="http://localhost:11434"
```

## 5. Initialize Database

```bash
# Create tables
python migrate.py init

# Seed with initial data
python migrate.py seed

# Or use Makefile
make migrate seed
```

## 6. Start the Server

```bash
# Production mode
python -m kimiclaw.cli.main serve

# Development mode with auto-reload
make dev

# Or directly
uvicorn kimiclaw.main:app --reload --host 0.0.0.0 --port 8000
```

## 7. Access the System

Open your browser to:

- **Dashboard**: http://localhost:8000/dashboard
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## CLI Commands

```bash
# Check system status
kimiclaw status

# Run lead generation
kimiclaw leads

# View configuration
kimiclaw config

# Ask the AI a question
kimiclaw ask "What's the weather like?"

# Check installed models
kimiclaw models
```

## Using Make Commands

```bash
make help        # Show all commands
make install     # Install dependencies
make test        # Run tests
make serve       # Start server
make status      # Show system status
make leads       # Run lead generation
make clean       # Clean build artifacts
```

## Configuring External Services

### Twilio (for voice calls)

1. Sign up at https://www.twilio.com
2. Get your Account SID and Auth Token
3. Buy a phone number
4. Add to `.env`:
```env
TWILIO_ACCOUNT_SID="your_account_sid"
TWILIO_AUTH_TOKEN="your_auth_token"
TWILIO_PHONE_NUMBER="+15555551234"
```

5. Configure webhook in Twilio console:
   - Voice: `http://your-domain.com/webhooks/twilio/voice`
   - SMS: `http://your-domain.com/webhooks/twilio/sms`

### Google Calendar & Gmail

1. Go to Google Cloud Console
2. Create a project and enable Calendar + Gmail APIs
3. Create OAuth 2.0 credentials
4. Download `credentials.json` to `credentials/google-credentials.json`
5. Add to `.env`:
```env
GOOGLE_CREDENTIALS_PATH="credentials/google-credentials.json"
GOOGLE_CALENDAR_ID="your-calendar-id@gmail.com"
GOOGLE_GMAIL_ADDRESS="your-email@gmail.com"
```

### SerpAPI (for lead generation)

1. Sign up at https://serpapi.com
2. Get your API key (free tier: 100 searches/month)
3. Add to `.env`:
```env
SERPAPI_KEY="your_api_key"
```

## Troubleshooting

### Database connection error
```bash
# Check PostgreSQL is running
docker-compose ps  # If using Docker
sudo systemctl status postgresql  # If local

# Reset database
python migrate.py reset
```

### Redis connection error
```bash
# Check Redis is running
redis-cli ping  # Should return "PONG"

# Restart Redis
docker-compose restart redis  # If using Docker
sudo systemctl restart redis-server  # If local
```

### Ollama model not found
```bash
# List installed models
ollama list

# Pull missing model
ollama pull llama3.2
```

### Import errors
```bash
# Reinstall in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py -v

# Run with coverage
pytest --cov=kimiclaw --cov-report=html
```

## Production Deployment

### Using systemd (Linux)

```bash
# The install.sh script creates this automatically
sudo systemctl start kimiclaw
sudo systemctl enable kimiclaw
sudo systemctl status kimiclaw
```

### Using Docker (Coming Soon)

```bash
docker build -t kimiclaw .
docker run -p 8000:8000 kimiclaw
```

## Next Steps

1. Configure external integrations (Twilio, Google, SerpAPI)
2. Customize business prompts in the code
3. Set up WhatsApp integration
4. Configure payment processing (Stripe/QuickBooks)
5. Deploy to production server
6. Set up monitoring and logging

## Support

- **Documentation**: See README.md
- **Issues**: https://github.com/yourusername/kimiclaw/issues
- **Email**: support@kimiclaw.com

---

**🐝 Built for trades. Proven in Montreal.**
