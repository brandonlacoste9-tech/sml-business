from setuptools import setup, find_packages

setup(
    name="kimiclaw",
    version="0.1.0",
    description="KimiClaw Business OS - Self-hosted AI business operating system for trades",
    author="KimiClaw",
    author_email="hello@kimiclaw.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "psycopg2-binary>=2.9.9",
        "sqlalchemy>=2.0.23",
        "alembic>=1.12.1",
        "redis>=5.0.1",
        "ollama>=0.1.6",
        "twilio>=8.10.3",
        "google-api-python-client>=2.108.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "serpapi>=0.1.5",
        "apscheduler>=3.10.4",
        "aiohttp>=3.9.1",
    ],
    entry_points={
        "console_scripts": [
            "kimiclaw=kimiclaw.cli:main",
        ],
    },
    python_requires=">=3.9",
)
