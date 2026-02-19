# API Reference

KimiClaw provides a REST API for webhooks, integrations, and programmatic access to business data.

**Base URL:** `http://localhost:8000` (configurable via `API_PORT`)

## Authentication

Currently uses IP allowlisting for webhooks. Full API key authentication coming in v0.2.0.

## Endpoints

### Health Check

Check system health and status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-19T12:00:00.000000",
  "business": "Montreal Plumbing Pros",
  "ollama": {
    "status": "healthy",
    "host": "http://localhost:11434",
    "models": ["llama3.2", "mistral", "llava:13b", "nomic-embed-text"]
  }
}
```

**Status Codes:**
- `200` - System healthy
- `503` - Service unavailable

---

### Twilio Voice Webhook

Receive incoming phone calls.

**Endpoint:** `POST /webhooks/twilio/voice`

**Request Body:**
```json
{
  "from_number": "+15145551234",
  "to_number": "+15145555000",
  "call_sid": "CA1234567890abcdef",
  "call_status": "ringing"
}
```

**Response:**
```json
{
  "message": "Call received",
  "customer_id": 42
}
```

**Status Codes:**
- `200` - Call logged successfully
- `400` - Invalid request
- `500` - Server error

---

### Twilio SMS Webhook

Receive incoming SMS messages.

**Endpoint:** `POST /webhooks/twilio/sms`

**Request Body:**
```json
{
  "from_number": "+15145551234",
  "to_number": "+15145555000",
  "body": "Do you do emergency repairs?",
  "message_sid": "SM1234567890abcdef"
}
```

**Response:**
```json
{
  "message": "SMS received",
  "response": "Yes, we offer 24/7 emergency plumbing services. What's your emergency?"
}
```

**Status Codes:**
- `200` - SMS processed
- `400` - Invalid request
- `500` - Server error

---

### Admin Command

Execute admin commands (typically via WhatsApp).

**Endpoint:** `POST /admin/command`

**Request Body:**
```json
{
  "command": "status",
  "user_id": "whatsapp:+15145551234"
}
```

**Commands:**

#### Status
```json
{
  "command": "status"
}
```

**Response:**
```json
{
  "command": "status",
  "fill_rate": 75.0,
  "mode": "normal",
  "jobs_today": 3,
  "revenue": 2450.00
}
```

#### Leads
```json
{
  "command": "leads"
}
```

**Response:**
```json
{
  "command": "leads",
  "count": 5,
  "leads": [
    {
      "name": "ABC Property Management",
      "score": 85,
      "opening_line": "Hi ABC, noticed your portfolio..."
    }
  ]
}
```

#### Boost
```json
{
  "command": "boost"
}
```

**Response:**
```json
{
  "command": "boost",
  "message": "Boost command received"
}
```

#### Pause
```json
{
  "command": "pause"
}
```

**Response:**
```json
{
  "command": "pause",
  "message": "Pause command received"
}
```

**Status Codes:**
- `200` - Command executed
- `400` - Unknown command
- `401` - Unauthorized
- `500` - Server error

---

### Get Customers

Retrieve all customers.

**Endpoint:** `GET /api/customers`

**Response:**
```json
{
  "customers": [
    {
      "id": 1,
      "name": "John Smith",
      "phone": "+15145551234",
      "email": "john@example.com",
      "address": "123 Main St, Montreal",
      "language_preference": "en",
      "lifetime_value": 2500.00,
      "total_jobs": 5,
      "created_at": "2025-01-15T10:00:00",
      "updated_at": "2026-02-19T12:00:00"
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

### Get Jobs

Retrieve jobs with optional status filter.

**Endpoint:** `GET /api/jobs?status={status}`

**Query Parameters:**
- `status` (optional) - Filter by status: `scheduled`, `in_progress`, `completed`, `cancelled`

**Response:**
```json
{
  "jobs": [
    {
      "id": 42,
      "customer_id": 1,
      "title": "Kitchen Sink Repair",
      "description": "Leaking pipe under sink",
      "service_type": "repair",
      "scheduled_start": "2026-02-20T14:00:00",
      "scheduled_end": "2026-02-20T16:00:00",
      "status": "scheduled",
      "estimated_price": 150.00,
      "is_emergency": false,
      "created_at": "2026-02-19T10:00:00"
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

### Get Leads

Retrieve leads with optional minimum score filter.

**Endpoint:** `GET /api/leads?min_score={score}`

**Query Parameters:**
- `min_score` (optional) - Minimum lead score (0-100), default: 0

**Response:**
```json
{
  "leads": [
    {
      "id": 15,
      "name": "ABC Property Management",
      "phone": "+15145551234",
      "email": "contact@abc.com",
      "address": "456 Downtown St",
      "source": "google_maps",
      "business_type": "property_management",
      "score": 85,
      "status": "new",
      "opening_line": "Hi ABC, noticed your portfolio includes buildings from the 1980s...",
      "created_at": "2026-02-19T08:00:00"
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

## Webhook Configuration

### Twilio Setup

1. Log in to [Twilio Console](https://console.twilio.com)
2. Go to Phone Numbers → Active Numbers
3. Select your number
4. Configure webhooks:
   - **Voice:** `https://your-domain.com/webhooks/twilio/voice`
   - **Messaging:** `https://your-domain.com/webhooks/twilio/sms`
5. Method: `POST`
6. Save configuration

### ngrok for Development

For local testing:

```bash
# Install ngrok
npm install -g ngrok

# Expose local API
ngrok http 8000

# Use ngrok URL in Twilio webhook configuration
# Example: https://abc123.ngrok.io/webhooks/twilio/voice
```

## Rate Limiting

Current limits (per minute):
- Health check: 60 requests
- Webhooks: 120 requests
- Admin commands: 30 requests
- Data endpoints: 60 requests

Rate limit headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1708347600
```

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "Missing required field: from_number",
    "details": {}
  }
}
```

**Common Error Codes:**
- `invalid_request` - Malformed request
- `not_found` - Resource not found
- `rate_limit_exceeded` - Too many requests
- `internal_error` - Server error
- `service_unavailable` - Dependency down (database, Ollama, etc.)

## CORS

CORS is enabled for all origins in development. Configure for production:

```python
# In src/kimiclaw/api/server.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Future API Features (v0.2.0)

- API key authentication
- Pagination for list endpoints
- Filtering and sorting
- GraphQL endpoint
- WebSocket support for real-time updates
- Bulk operations
- Export endpoints (CSV, JSON)

## Examples

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Get customers
curl http://localhost:8000/api/customers

# Get hot leads
curl http://localhost:8000/api/leads?min_score=70

# Admin command
curl -X POST http://localhost:8000/admin/command \
  -H "Content-Type: application/json" \
  -d '{"command": "status", "user_id": "admin"}'
```

### Python

```python
import requests

# Get status
response = requests.get("http://localhost:8000/health")
print(response.json())

# Get leads
response = requests.get("http://localhost:8000/api/leads", params={"min_score": 70})
leads = response.json()["leads"]
for lead in leads:
    print(f"{lead['name']}: {lead['score']}")
```

### JavaScript

```javascript
// Get jobs
fetch('http://localhost:8000/api/jobs?status=scheduled')
  .then(response => response.json())
  .then(data => {
    console.log(`${data.jobs.length} scheduled jobs`);
  });

// Send admin command
fetch('http://localhost:8000/admin/command', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ command: 'status', user_id: 'admin' })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Next Steps

- [Configuration Guide](configuration.md)
- [CLI Usage](cli-usage.md)
- [Architecture Overview](architecture.md)
