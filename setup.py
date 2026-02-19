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
)
