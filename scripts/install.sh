#!/bin/bash
#
# KimiClaw Business OS Installation Script
# Usage: curl -fsSL https://get.kimiclaw.com/install.sh | bash
#

set -e

KIMICLAW_VERSION="0.1.0"
INSTALL_DIR="$HOME/.kimiclaw"

echo "🐝 KimiClaw Business OS Installer v${KIMICLAW_VERSION}"
echo "================================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    PKG_MANAGER="apt"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    PKG_MANAGER="brew"
else
    echo "❌ Unsupported OS: $OSTYPE"
    echo "KimiClaw supports Linux and macOS (Windows via WSL2)"
    exit 1
fi

echo "✓ Detected OS: $OS"

# Check RAM
TOTAL_RAM=$(free -g 2>/dev/null | awk '/^Mem:/{print $2}' || sysctl -n hw.memsize 2>/dev/null | awk '{print int($1/1024/1024/1024)}')
if [ "$TOTAL_RAM" -ge 16 ]; then
    MODE="full"
    echo "✓ RAM: ${TOTAL_RAM}GB - Full Mode (with photo analysis)"
elif [ "$TOTAL_RAM" -ge 8 ]; then
    MODE="lite"
    echo "✓ RAM: ${TOTAL_RAM}GB - Lite Mode (without photo analysis)"
else
    echo "⚠️  Warning: ${TOTAL_RAM}GB RAM detected. Minimum 8GB recommended."
    MODE="lite"
fi

# Install dependencies
echo ""
echo "Installing system dependencies..."

if [ "$OS" == "linux" ]; then
    sudo apt-get update -qq
    sudo apt-get install -y python3 python3-pip python3-venv postgresql redis curl git
elif [ "$OS" == "macos" ]; then
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install from https://brew.sh"
        exit 1
    fi
    brew install python postgresql redis git
fi

echo "✓ System dependencies installed"

# Install Ollama
echo ""
echo "Installing Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.ai/install.sh | sh
    echo "✓ Ollama installed"
else
    echo "✓ Ollama already installed"
fi

# Start Ollama service
ollama serve > /dev/null 2>&1 &
sleep 2

# Download AI models
echo ""
echo "Downloading AI models (this may take 10-30 minutes)..."
ollama pull llama3.2
ollama pull mistral
ollama pull nomic-embed-text

if [ "$MODE" == "full" ]; then
    ollama pull llava:13b
fi

echo "✓ AI models downloaded"

# Create installation directory
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Clone or download KimiClaw
echo ""
echo "Downloading KimiClaw..."
if [ -d ".git" ]; then
    git pull
else
    git clone https://github.com/brandonlacoste9-tech/sml-business.git .
fi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

echo "✓ KimiClaw installed"

# Interactive setup
echo ""
echo "================================================"
echo "Business Configuration"
echo "================================================"
echo "Please answer these 8 questions:"
echo ""

read -p "1. Business Name: " BUSINESS_NAME
read -p "2. Industry (plumbing/electrical/hvac/landscaping/cleaning): " BUSINESS_INDUSTRY
read -p "3. Phone Number: " BUSINESS_PHONE
read -p "4. WhatsApp Number: " BUSINESS_WHATSAPP
read -p "5. Business Hours Start (HH:MM): " BUSINESS_HOURS_START
read -p "6. Business Hours End (HH:MM): " BUSINESS_HOURS_END
read -p "7. Daily Capacity (jobs per day): " BUSINESS_CAPACITY
read -p "8. Language (en/fr/bilingual): " BUSINESS_LANGUAGE

# Create .env file
cat > .env << EOF
# KimiClaw Business OS Configuration
BUSINESS_NAME="${BUSINESS_NAME}"
BUSINESS_INDUSTRY="${BUSINESS_INDUSTRY}"
BUSINESS_PHONE="${BUSINESS_PHONE}"
BUSINESS_WHATSAPP="${BUSINESS_WHATSAPP}"
BUSINESS_HOURS_START="${BUSINESS_HOURS_START}"
BUSINESS_HOURS_END="${BUSINESS_HOURS_END}"
BUSINESS_CAPACITY=${BUSINESS_CAPACITY}
BUSINESS_LANGUAGE="${BUSINESS_LANGUAGE}"

# Database
DATABASE_URL="postgresql://kimiclaw:kimiclaw123@localhost:5432/kimiclaw"
REDIS_URL="redis://localhost:6379/0"

# Ollama
OLLAMA_HOST="http://localhost:11434"
OLLAMA_CONVERSATION_MODEL="llama3.2"
OLLAMA_REASONING_MODEL="mistral"
OLLAMA_VISION_MODEL="llava:13b"
OLLAMA_EMBEDDING_MODEL="nomic-embed-text"
EOF

echo "✓ Configuration saved"

# Setup database
echo ""
echo "Setting up database..."
sudo -u postgres psql -c "CREATE DATABASE kimiclaw;" 2>/dev/null || true
sudo -u postgres psql -c "CREATE USER kimiclaw WITH PASSWORD 'kimiclaw123';" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE kimiclaw TO kimiclaw;" 2>/dev/null || true

# Initialize database
python -m kimiclaw.cli init

echo "✓ Database initialized"

# Create systemd service (Linux only)
if [ "$OS" == "linux" ]; then
    cat > /tmp/kimiclaw.service << EOF
[Unit]
Description=KimiClaw Business OS
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/python -m kimiclaw.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    sudo mv /tmp/kimiclaw.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable kimiclaw
    sudo systemctl start kimiclaw
    
    echo "✓ Service installed and started"
fi

# Add CLI to PATH
if ! grep -q "$INSTALL_DIR/venv/bin" ~/.bashrc; then
    echo "export PATH=\"$INSTALL_DIR/venv/bin:\$PATH\"" >> ~/.bashrc
    echo "✓ CLI added to PATH (restart shell or run: source ~/.bashrc)"
fi

echo ""
echo "================================================"
echo "🐝 Installation Complete!"
echo "================================================"
echo ""
echo "Your AI business assistant is now running!"
echo ""
echo "Next steps:"
echo "1. Check status: kimiclaw status"
echo "2. View leads: kimiclaw leads list"
echo "3. Check health: kimiclaw health"
echo ""
echo "For Twilio integration (phone/SMS):"
echo "  - Sign up at https://twilio.com"
echo "  - Add credentials to $INSTALL_DIR/.env"
echo ""
echo "Documentation: https://github.com/brandonlacoste9-tech/sml-business"
echo ""
echo "🐝 Built for trades. Proven in Montreal."
