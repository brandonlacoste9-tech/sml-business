"""Setup configuration for KimiClaw Business OS."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kimiclaw",
    version="0.1.0",
    author="KimiClaw Team",
    author_email="support@kimiclaw.com",
    description="Your AI. Your data. Your business. 🐝 Self-hosted AI business operating system for trades.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kimiclaw",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "kimiclaw=kimiclaw.cli.main:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "kimiclaw": ["*.json", "*.yaml"],
    },
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
