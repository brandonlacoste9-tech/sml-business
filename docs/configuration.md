# Configuration Guide

## Environment Variables

KimiClaw is configured through environment variables, typically stored in a `.env` file at the root of your installation.

## Configuration File Location

- **Development:** `.env` in project root
- **Production:** `$HOME/.kimiclaw/.env`

## Core Settings

### Business Information

```bash
# Your business name (displayed in all communications)
BUSINESS_NAME="Your Business Name"

# Industry type (affects AI prompts and lead scoring)
# Options: plumbing, electrical, hvac, landscaping, cleaning, general_contractor
BUSINESS_INDUSTRY="plumbing"

# Phone number for business (format: +1234567890)
BUSINESS_PHONE="+15551234567"

# WhatsApp number for admin notifications
BUSINESS_WHATSAPP="+15551234567"

# Operating hours (24-hour format)
BUSINESS_HOURS_START="08:00"
BUSINESS_HOURS_END="18:00"

# Daily job capacity (used for fill rate calculation)
BUSINESS_CAPACITY=10

# Language preference
# Options: en (English), fr (French), bilingual
BUSINESS_LANGUAGE="en"
```

### Database Configuration

```bash
# PostgreSQL connection string
DATABASE_URL="postgresql://username:password@localhost:5432/kimiclaw"

# Redis connection string
REDIS_URL="redis://localhost:6379/0"
```

### Ollama AI Configuration

```bash
# Ollama server URL
OLLAMA_HOST="http://localhost:11434"

# Model for conversations (calls, SMS, email)
OLLAMA_CONVERSATION_MODEL="llama3.2"

# Model for reasoning (lead scoring, analysis)
OLLAMA_REASONING_MODEL="mistral"

# Model for image analysis (requires 16GB+ RAM)
OLLAMA_VISION_MODEL="llava:13b"

# Model for embeddings (customer memory)
OLLAMA_EMBEDDING_MODEL="nomic-embed-text"
```

### External Services

#### Twilio (Required for phone/SMS)

```bash
TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN="your_auth_token"
TWILIO_PHONE_NUMBER="+15551234567"
```

Sign up at [twilio.com](https://twilio.com) and get credentials from the Console.

#### SerpAPI (Required for lead generation)

```bash
SERPAPI_KEY="your_serpapi_key"
```

Sign up at [serpapi.com](https://serpapi.com) - free tier includes 100 searches/month.

#### Google Calendar (Optional)

```bash
GOOGLE_CALENDAR_CREDENTIALS_PATH="/path/to/credentials.json"
```

Set up OAuth2 credentials at [Google Cloud Console](https://console.cloud.google.com).

#### Gmail (Optional)

```bash
GOOGLE_GMAIL_CREDENTIALS_PATH="/path/to/gmail_credentials.json"
```

Use the same OAuth2 process as Google Calendar.

#### Payment Processing (Optional)

```bash
# QuickBooks
QUICKBOOKS_CLIENT_ID="your_client_id"
QUICKBOOKS_CLIENT_SECRET="your_client_secret"

# Stripe
STRIPE_API_KEY="sk_test_..."
```

### Application Settings

```bash
# Web dashboard port
APP_PORT=3000

# API server port
API_PORT=8000

# Debug mode (true/false)
DEBUG=false

# Logging level
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL="INFO"
```

### Pricing Configuration

```bash
# Pricing mode
# Options: fixed, dynamic
PRICING_MODE="dynamic"

# Default hourly rate (CAD)
DEFAULT_HOURLY_RATE=75

# Surge pricing multiplier (when calendar > 90% full)
SURGE_PRICING_MULTIPLIER=1.3
```

## Example Configurations

### Minimal (Development)

```bash
BUSINESS_NAME="Test Plumbing"
BUSINESS_INDUSTRY="plumbing"
BUSINESS_CAPACITY=5
DATABASE_URL="postgresql://localhost/kimiclaw"
REDIS_URL="redis://localhost:6379/0"
OLLAMA_HOST="http://localhost:11434"
```

### Full Production Setup

```bash
# Business
BUSINESS_NAME="Montreal Plumbing Pros"
BUSINESS_INDUSTRY="plumbing"
BUSINESS_PHONE="+15145551234"
BUSINESS_WHATSAPP="+15145551234"
BUSINESS_HOURS_START="07:00"
BUSINESS_HOURS_END="19:00"
BUSINESS_CAPACITY=15
BUSINESS_LANGUAGE="bilingual"

# Database
DATABASE_URL="postgresql://kimiclaw:secure_password@localhost:5432/kimiclaw_prod"
REDIS_URL="redis://:redis_password@localhost:6379/0"

# Ollama
OLLAMA_HOST="http://localhost:11434"
OLLAMA_CONVERSATION_MODEL="llama3.2"
OLLAMA_REASONING_MODEL="mistral"
OLLAMA_VISION_MODEL="llava:13b"
OLLAMA_EMBEDDING_MODEL="nomic-embed-text"

# Twilio
TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN="your_token"
TWILIO_PHONE_NUMBER="+15145555000"

# SerpAPI
SERPAPI_KEY="your_key"

# Google
GOOGLE_CALENDAR_CREDENTIALS_PATH="/home/kimiclaw/.credentials/calendar.json"
GOOGLE_GMAIL_CREDENTIALS_PATH="/home/kimiclaw/.credentials/gmail.json"

# Stripe
STRIPE_API_KEY="sk_live_..."

# App
APP_PORT=3000
API_PORT=8000
DEBUG=false
LOG_LEVEL="INFO"
PRICING_MODE="dynamic"
DEFAULT_HOURLY_RATE=85
SURGE_PRICING_MULTIPLIER=1.4
```

## Security Best Practices

1. **Never commit `.env` files to version control**
2. **Use strong database passwords**
3. **Restrict Redis to localhost or use authentication**
4. **Keep API keys secure and rotate regularly**
5. **Use HTTPS in production for all external services**
6. **Set appropriate file permissions:** `chmod 600 .env`

## Validation

After configuration, verify settings:

```bash
kimiclaw health
```

This checks:
- Ollama connection and available models
- Database connection
- Redis connection

## Troubleshooting

### Configuration Not Loading

```bash
# Check .env exists
ls -la .env

# Check permissions
chmod 600 .env

# Verify environment variables
python3 -c "from kimiclaw.core.config import settings; print(settings.business_name)"
```

### Database Connection Errors

```bash
# Test PostgreSQL connection
psql -h localhost -U kimiclaw -d kimiclaw -c "SELECT 1;"

# Check DATABASE_URL format
echo $DATABASE_URL
```

### Ollama Not Responding

```bash
# Check Ollama is running
ps aux | grep ollama

# Test Ollama connection
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve &
```

## Next Steps

- [CLI Usage Guide](cli-usage.md)
- [API Reference](api-reference.md)
- [Architecture Overview](architecture.md)
