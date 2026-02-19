# Contributing to KimiClaw Business OS

Thank you for your interest in contributing to KimiClaw! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Keep discussions professional and on-topic

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/kimiclaw.git
cd kimiclaw

# Add upstream remote
git remote add upstream https://github.com/yourusername/kimiclaw.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Install dev dependencies
pip install pytest pytest-asyncio pytest-cov black flake8

# Start infrastructure
docker-compose up -d

# Initialize database
python migrate.py init
python migrate.py seed
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py -v

# Run with coverage
pytest --cov=kimiclaw --cov-report=html

# Using Makefile
make test
make test-cov
```

### Code Formatting

We use Black for code formatting:

```bash
# Format all code
black kimiclaw/ tests/

# Or use Makefile
make format

# Check formatting without making changes
black --check kimiclaw/ tests/
```

### Linting

We use flake8 for linting:

```bash
# Lint code
flake8 kimiclaw/ tests/ --max-line-length=100

# Or use Makefile
make lint
```

### Testing Your Changes

```bash
# Start the server
make dev

# In another terminal, test CLI commands
python -m kimiclaw.cli.main status
python -m kimiclaw.cli.main config

# Check the web interface
# http://localhost:8000/dashboard
```

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use type hints where possible
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

Example:

```python
from typing import Optional, List

def calculate_fill_rate(
    start_date: datetime,
    end_date: datetime,
    capacity: int
) -> float:
    """Calculate calendar fill rate.
    
    Args:
        start_date: Start date for calculation
        end_date: End date for calculation
        capacity: Total available capacity in hours
        
    Returns:
        Fill rate from 0.0 to 1.0
        
    Raises:
        ValueError: If dates are invalid
    """
    # Implementation here
    pass
```

### Project Structure

```
kimiclaw/
├── core/           # Core functionality (config, AI client)
├── modules/        # Autonomous loops
├── models/         # Database models
├── integrations/   # External service integrations
├── utils/          # Utility functions
└── cli/            # CLI interface
```

### Commit Messages

Follow conventional commits format:

```
feat: add WhatsApp integration
fix: resolve calendar sync issue
docs: update installation guide
test: add tests for lead generation
refactor: simplify database queries
chore: update dependencies
```

## Types of Contributions

### Bug Reports

When reporting bugs, include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and logs

Use the bug report template on GitHub.

### Feature Requests

When requesting features:

- Describe the use case
- Explain the expected behavior
- Consider implementation approach
- Note any related issues

Use the feature request template on GitHub.

### Code Contributions

#### Priority Areas

High priority contributions:

1. **External Integrations**
   - WhatsApp Business API
   - SerpAPI lead scraping
   - QuickBooks Online
   - Stripe payments

2. **Core Features**
   - Advertising campaign loop
   - Financial reconciliation loop
   - Enhanced dashboard with real metrics
   - Email templates system

3. **Testing**
   - Integration tests
   - End-to-end tests
   - Performance tests

4. **Documentation**
   - API documentation
   - User guides
   - Video tutorials

#### Making Changes

1. Write tests first (TDD approach preferred)
2. Implement your changes
3. Ensure all tests pass
4. Update documentation
5. Add changelog entry if applicable

### Documentation

Documentation improvements are always welcome:

- Fix typos and clarify language
- Add examples and use cases
- Improve installation instructions
- Create guides and tutorials

## Pull Request Process

### Before Submitting

1. Sync with upstream:
```bash
git fetch upstream
git rebase upstream/main
```

2. Run all checks:
```bash
make test
make lint
make format
```

3. Update documentation if needed

4. Add tests for new functionality

### Submitting

1. Push to your fork:
```bash
git push origin feature/your-feature-name
```

2. Create pull request on GitHub

3. Fill out the PR template completely

4. Link related issues

### PR Review

- Address all review comments
- Keep the PR focused and small
- Respond to feedback promptly
- Be open to suggestions

### After Merge

- Delete your feature branch
- Pull latest changes from upstream
- Celebrate your contribution! 🎉

## Architecture Guidelines

### Async/Await

Use async functions for I/O operations:

```python
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### Error Handling

Always handle exceptions gracefully:

```python
try:
    result = await risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    return default_value
```

### Logging

Use loguru for logging:

```python
from loguru import logger

logger.info("Operation started")
logger.warning("Unusual condition detected")
logger.error(f"Error occurred: {error}")
```

### Configuration

Use settings from config:

```python
from kimiclaw.core.config import settings

if settings.is_full_mode:
    # Use vision model
    pass
```

## Testing Guidelines

### Unit Tests

Test individual functions and classes:

```python
def test_calculate_fill_rate():
    """Test fill rate calculation."""
    rate = calculate_fill_rate(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 7),
        capacity=40
    )
    assert 0.0 <= rate <= 1.0
```

### Integration Tests

Test module interactions:

```python
@pytest.mark.asyncio
async def test_lead_generation_pipeline():
    """Test complete lead generation flow."""
    loop = LeadGenerationLoop()
    await loop.run_daily_hunt()
    # Verify leads were created in database
```

### Mock External Services

Use mocks for external APIs:

```python
@patch('httpx.AsyncClient.post')
async def test_ollama_generate(mock_post):
    mock_post.return_value.json.return_value = {"response": "Hello"}
    result = await ollama.generate("Hi")
    assert result["response"] == "Hello"
```

## Questions?

- Open a discussion on GitHub
- Check existing issues and PRs
- Read the documentation
- Ask in the community chat

Thank you for contributing to KimiClaw! 🐝
