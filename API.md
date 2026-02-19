# KimiClaw API Documentation

## Base URL

```
http://localhost:8000
```

For production, replace with your actual domain.

## Authentication

Currently, the API does not require authentication for webhooks. In production, implement:

- Twilio signature verification for webhooks
- API key authentication for admin endpoints
- OAuth2 for Google integrations

## Core Endpoints

### Health Check

Check if the system is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "business": "Your Business Name",
  "mode": "lite"
}
```

**Status Codes**:
- `200 OK` - System is healthy

---

### System Status

Get current system metrics and status.

**Endpoint**: `GET /api/status`

**Response**:
```json
{
  "business_name": "Your Business Name",
  "mode": "lite",
  "calendar_fill_rate": 0.65,
  "calls_today": 12,
  "leads_today": 3,
  "revenue_today": 1250.00
}
```

**Status Codes**:
- `200 OK` - Success

---

## Webhook Endpoints

### Twilio Voice Webhook

Handles incoming phone calls via Twilio.

**Endpoint**: `POST /webhooks/twilio/voice`

**Content-Type**: `application/x-www-form-urlencoded`

**Request Parameters** (from Twilio):
- `From` - Caller's phone number
- `To` - Called phone number (your business number)
- `CallSid` - Unique call identifier
- `CallStatus` - Call status (ringing, in-progress, completed)

**Response**: TwiML XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice" language="en-CA">
    Thank you for calling Your Business Name. Please hold while we connect you.
  </Say>
</Response>
```

**Configuration in Twilio Console**:
1. Go to Phone Numbers → Active Numbers
2. Select your number
3. Under Voice & Fax → "A CALL COMES IN"
4. Set to: `http://your-domain.com/webhooks/twilio/voice`
5. HTTP Method: POST

---

### Twilio SMS Webhook

Handles incoming SMS messages via Twilio.

**Endpoint**: `POST /webhooks/twilio/sms`

**Content-Type**: `application/x-www-form-urlencoded`

**Request Parameters** (from Twilio):
- `From` - Sender's phone number
- `To` - Recipient phone number (your business number)
- `Body` - Message text
- `MessageSid` - Unique message identifier

**Response**: TwiML XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>Thanks for contacting Your Business Name. We'll get back to you shortly!</Message>
</Response>
```

**Configuration in Twilio Console**:
1. Go to Phone Numbers → Active Numbers
2. Select your number
3. Under Messaging → "A MESSAGE COMES IN"
4. Set to: `http://your-domain.com/webhooks/twilio/sms`
5. HTTP Method: POST

---

## Web Interfaces

### Root Page

Landing page with system status.

**Endpoint**: `GET /`

**Response**: HTML page with:
- Business name
- System mode (Lite/Full)
- Online status
- Links to dashboard and docs

---

### Dashboard

Real-time business metrics dashboard.

**Endpoint**: `GET /dashboard`

**Response**: HTML page with:
- Calendar fill rate
- Calls handled today
- Leads generated today
- Revenue today
- Current system mode
- System status

**Auto-refresh**: Every 30 seconds

---

### API Documentation

Interactive API documentation via FastAPI/Swagger.

**Endpoint**: `GET /docs`

**Response**: Swagger UI with:
- All available endpoints
- Request/response schemas
- Try-it-out functionality
- Authentication requirements

**Alternative**: `GET /redoc` for ReDoc format

---

## Future Endpoints (Coming Soon)

### Customers API

```
GET    /api/customers          # List all customers
POST   /api/customers          # Create customer
GET    /api/customers/{id}     # Get customer details
PUT    /api/customers/{id}     # Update customer
DELETE /api/customers/{id}     # Delete customer
```

### Appointments API

```
GET    /api/appointments       # List appointments
POST   /api/appointments       # Book appointment
GET    /api/appointments/{id}  # Get appointment details
PUT    /api/appointments/{id}  # Update appointment
DELETE /api/appointments/{id}  # Cancel appointment
```

### Leads API

```
GET    /api/leads              # List leads
POST   /api/leads/hunt         # Trigger lead hunt
GET    /api/leads/{id}         # Get lead details
PUT    /api/leads/{id}         # Update lead status
POST   /api/leads/{id}/contact # Mark lead as contacted
```

### Invoices API

```
GET    /api/invoices           # List invoices
POST   /api/invoices           # Create invoice
GET    /api/invoices/{id}      # Get invoice details
POST   /api/invoices/{id}/send # Send invoice to customer
POST   /api/invoices/{id}/pay  # Mark invoice as paid
```

### Admin API

```
GET    /api/admin/status       # Detailed system status
POST   /api/admin/mode         # Change system mode (hunter/surge)
GET    /api/admin/metrics      # Historical metrics
POST   /api/admin/test-email   # Send test email
POST   /api/admin/test-sms     # Send test SMS
```

---

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "status_code": 400
}
```

**Common Status Codes**:
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Rate Limiting

Currently no rate limiting. In production, implement:

- 100 requests per minute per IP for public endpoints
- 1000 requests per minute for authenticated users
- Webhooks not rate limited (trusted sources only)

---

## WebSocket API (Coming Soon)

Real-time updates via WebSocket:

**Endpoint**: `WS /ws/status`

**Messages**:
```json
{
  "type": "status_update",
  "data": {
    "calendar_fill_rate": 0.67,
    "calls_today": 15,
    "revenue_today": 1500.00
  }
}
```

---

## CLI as API

The CLI can be used for scripting:

```bash
# Get status (JSON output)
kimiclaw status --json

# Trigger lead hunt
kimiclaw leads --count 20

# Query AI
kimiclaw ask "What's my calendar like today?"
```

---

## Integration Examples

### Python

```python
import httpx

# Check health
response = httpx.get("http://localhost:8000/health")
print(response.json())

# Get status
response = httpx.get("http://localhost:8000/api/status")
status = response.json()
print(f"Fill rate: {status['calendar_fill_rate']}")
```

### JavaScript

```javascript
// Check health
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Get status
fetch('http://localhost:8000/api/status')
  .then(response => response.json())
  .then(data => console.log('Fill rate:', data.calendar_fill_rate));
```

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Get status
curl http://localhost:8000/api/status

# Simulate Twilio voice webhook
curl -X POST http://localhost:8000/webhooks/twilio/voice \
  -d "From=+15551234567" \
  -d "To=+15559876543" \
  -d "CallSid=CA1234567890"
```

---

## Security Best Practices

1. **Use HTTPS in production** - Never expose HTTP in production
2. **Verify Twilio signatures** - Validate webhook authenticity
3. **Implement API authentication** - Protect admin endpoints
4. **Rate limit webhooks** - Prevent abuse
5. **Sanitize inputs** - Prevent injection attacks
6. **Log all access** - Audit trail for security events
7. **Use environment variables** - Never commit secrets

---

## Support

- **Documentation**: See README.md
- **Issues**: https://github.com/yourusername/kimiclaw/issues
- **Email**: support@kimiclaw.com

---

**🐝 Built for trades. Proven in Montreal.**
