# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Security Updates

### Latest (2026-02-19)

All security vulnerabilities have been addressed:

**Fixed Vulnerabilities:**

1. **aiohttp 3.9.1 → 3.13.3**
   - ✅ CVE: Zip bomb vulnerability in HTTP Parser auto_decompress
   - ✅ CVE: DoS when parsing malformed POST requests  
   - ✅ CVE: Directory traversal vulnerability

2. **fastapi 0.104.1 → 0.109.1**
   - ✅ CVE: Content-Type Header ReDoS vulnerability

3. **python-multipart 0.0.6 → 0.0.22**
   - ✅ CVE: Arbitrary file write vulnerability
   - ✅ CVE: DoS via deformed multipart/form-data boundary
   - ✅ CVE: Content-Type Header ReDoS vulnerability

**Current Status:** ✅ No known vulnerabilities (verified with CodeQL and GitHub Advisory Database)

## Reporting a Vulnerability

If you discover a security vulnerability in KimiClaw Business OS, please report it by:

1. **DO NOT** open a public GitHub issue
2. Email: security@kimiclaw.com (or hello@kimiclaw.com)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We aim to respond within 48 hours and will keep you updated on the fix progress.

## Security Best Practices

When deploying KimiClaw:

### Environment & Configuration
- ✅ Never commit `.env` files to version control
- ✅ Use strong database passwords
- ✅ Restrict Redis to localhost or use authentication
- ✅ Set file permissions: `chmod 600 .env`
- ✅ Keep API keys secure and rotate regularly

### Network Security
- ✅ Use HTTPS in production for all external services
- ✅ Configure CORS properly (don't use `allow_origins=["*"]` in production)
- ✅ Use webhook signature verification for Twilio
- ✅ Restrict API access by IP when possible

### Database Security
- ✅ Use database connection pooling
- ✅ Enable PostgreSQL SSL connections in production
- ✅ Regular database backups
- ✅ Principle of least privilege for database users

### AI & Data Privacy
- ✅ All AI runs locally via Ollama (no data sent to cloud)
- ✅ Customer data never leaves your infrastructure
- ✅ Regular audit of data retention policies
- ✅ Implement data encryption at rest

### Dependencies
- ✅ Regularly update dependencies: `pip install -U -r requirements.txt`
- ✅ Monitor security advisories
- ✅ Run security scans: `pip-audit` or `safety check`
- ✅ Review dependency licenses

### Deployment
- ✅ Run as non-root user
- ✅ Use systemd or similar for service management
- ✅ Configure firewall (ufw/iptables)
- ✅ Regular system updates
- ✅ Monitor logs for suspicious activity

## Security Features

KimiClaw includes:

- **Local AI Inference** - No data sent to external AI providers
- **Type Safety** - Pydantic validation prevents injection attacks
- **Session Management** - Proper database connection cleanup
- **Input Validation** - FastAPI request validation
- **Structured Logging** - Audit trail of all operations
- **Environment-based Secrets** - No hardcoded credentials

## Audit History

| Date       | Action                              | Status |
|------------|-------------------------------------|--------|
| 2026-02-19 | Initial security scan (CodeQL)      | ✅ Pass |
| 2026-02-19 | Code review (9 issues found)        | ✅ Fixed |
| 2026-02-19 | Dependency vulnerabilities (7 CVEs) | ✅ Fixed |
| 2026-02-19 | Final security verification         | ✅ Pass |

## Security Contacts

- Security Email: security@kimiclaw.com
- General Support: hello@kimiclaw.com
- GitHub Issues: https://github.com/brandonlacoste9-tech/sml-business/issues

---

*Last updated: 2026-02-19*
*Version: 0.1.0*
