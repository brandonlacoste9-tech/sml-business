# Installation Guide

## Prerequisites

- Linux, macOS, or Windows with WSL2
- 8GB RAM minimum (16GB+ for Full Mode with photo analysis)
- PostgreSQL 12+
- Redis 6+
- Python 3.9+

## Quick Installation

Run the installation script:

```bash
curl -fsSL https://get.kimiclaw.com/install.sh | bash
```

The installer will:
1. Detect your OS and RAM
2. Install system dependencies
3. Install Ollama and download AI models
4. Set up PostgreSQL and Redis
5. Ask you 8 configuration questions
6. Initialize the database
7. Start the service

**Total time: 20-45 minutes** (varies based on internet speed for AI model downloads)

## Manual Installation

If you prefer manual installation, see the detailed steps in the main README.

## Next Steps

- [Configuration Guide](configuration.md)
- [CLI Usage](cli-usage.md)
- [API Reference](api-reference.md)
