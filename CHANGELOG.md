# Changelog

All notable changes to KimiClaw Business OS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-02-19

### Added

#### Core System
- Initial project structure with modular architecture
- Python package configuration with setup.py
- Comprehensive configuration management via pydantic-settings
- Environment variable configuration with .env support
- Automatic system mode detection (Lite/Full based on RAM)

#### AI Integration
- Ollama client wrapper with full API support
- Model routing (llama3.2, mistral, llava, nomic-embed-text)
- Text generation and chat conversation methods
- Image analysis with vision models (Full Mode)
- Embedding generation for semantic search
- Automatic model detection and listing

#### Database
- PostgreSQL models for customers, appointments, leads, interactions, invoices
- Business metrics tracking model
- System configuration key-value store
- Database initialization and migration utilities
- Session management with context managers
- SQLAlchemy ORM integration

#### Redis & Memory
- Redis client for caching and customer memory
- Customer interaction storage with embeddings
- Semantic memory search using cosine similarity
- Vector-based customer preference tracking

#### Autonomous Loops
- Business Intelligence Loop (5-minute interval)
  - Calendar fill rate monitoring
  - Automatic mode switching (Normal/Hunter/Surge)
  - Health metrics tracking
- Communication Handler Loop (30-second interval)
  - Email processing queue
  - SMS processing queue
  - Call handling coordination
- Lead Generation Loop (daily at 8am)
  - Automated lead searching
  - AI-powered lead scoring (0-100)
  - Personalized opening line generation
  - Hot lead filtering (score >= 70)

#### FastAPI Server
- Main application server with async lifecycle
- Root endpoint with system status HTML page
- Interactive web dashboard at /dashboard
- Health check endpoint
- System status API endpoint
- Twilio webhook endpoints (voice, SMS)
- Automatic API documentation at /docs

#### Google Integrations
- Google Calendar API client
  - Event creation and management
  - Calendar fill rate calculation
  - Multi-day event querying
  - Business hours awareness
- Gmail API client
  - Email sending (text and HTML)
  - Unread message retrieval
  - Message marking (read/unread)
  - OAuth2 authentication flow

#### CLI Tool
- Rich terminal UI with colors and tables
- Commands:
  - `status` - Show system status and metrics
  - `leads` - Run lead generation hunt
  - `config` - Display configuration
  - `serve` - Start FastAPI server
  - `ask` - Ask AI a question
  - `models` - List Ollama models
  - `install` - Interactive setup wizard
- Interactive 8-question onboarding
- Configuration file generation

#### Installation
- Cross-platform installation script (install.sh)
  - OS detection (Ubuntu, Debian, macOS)
  - RAM detection for mode selection
  - Automatic dependency installation
  - Ollama installation and model downloading
  - PostgreSQL and Redis setup
  - Systemd service creation (Linux)
  - Database initialization
- Database migration script (migrate.py)
  - init, reset, and seed commands
  - Safe data handling with confirmations

#### Development Tools
- Makefile with 15+ common commands
- Docker Compose for PostgreSQL and Redis
- Pytest configuration with fixtures
- Unit tests for config and Ollama client
- .gitignore for Python projects
- Example environment file (.env.example)

#### Documentation
- Comprehensive README with feature overview
- Quick Start guide (QUICKSTART.md)
- Contributing guidelines (CONTRIBUTING.md)
- API documentation via FastAPI
- Inline code documentation and docstrings
- System architecture diagrams in README

### Architecture Decisions

- **Local-first AI**: All AI processing via Ollama (no cloud APIs)
- **Async-first**: FastAPI and asyncio for concurrent operations
- **Mode-based operation**: Automatic adjustment based on calendar capacity
- **Modular design**: Clean separation of concerns
- **Configuration over code**: Environment-based configuration
- **Developer experience**: Rich CLI, comprehensive docs, easy setup

### Technical Stack

- **Backend**: Python 3.9+, FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **Cache**: Redis
- **AI**: Ollama (local LLM runtime)
- **Testing**: pytest, pytest-asyncio
- **CLI**: Click, Rich, Typer
- **HTTP**: httpx, aiohttp
- **External APIs**: Twilio, Google Calendar/Gmail, SerpAPI

### Known Limitations

- WhatsApp integration is stubbed (not implemented)
- SerpAPI lead scraping is placeholder
- QuickBooks/Stripe integrations are stubbed
- Advertising loop not implemented
- Financial reconciliation loop not implemented
- Dashboard shows static data (not live from database)
- No Alembic migrations yet
- Email templates not implemented
- No monitoring/alerting system

## [Unreleased]

### Planned

#### Short Term
- Complete SerpAPI lead generation integration
- Implement WhatsApp Business API
- Add advertising campaign loop
- Add financial reconciliation loop
- Connect dashboard to live database metrics
- Add Alembic database migrations
- Create email template system

#### Medium Term
- QuickBooks Online integration
- Stripe payment processing
- Docker image for deployment
- Integration tests
- Performance optimization
- Real-time WebSocket dashboard updates
- Mobile app for iOS/Android

#### Long Term
- Multi-language support beyond EN/FR
- Machine learning model fine-tuning
- Voice AI with real-time transcription
- Advanced analytics and reporting
- White-label customization
- Franchise management features
- API for third-party integrations

---

**Format**: [Version] - Date (YYYY-MM-DD)
**Types**: Added, Changed, Deprecated, Removed, Fixed, Security
