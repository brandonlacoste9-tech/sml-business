#!/bin/bash
# KimiClaw Business OS - Installation Script
# Usage: curl -fsSL https://get.kimiclaw.com/install.sh | bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print with emoji
print_header() {
    echo -e "${BLUE}🐝 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$ID
            VER=$VERSION_ID
        else
            OS="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    
    echo "$OS"
}

# Check system RAM
check_ram() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        TOTAL_RAM=$(sysctl -n hw.memsize | awk '{print int($1/1024/1024/1024)}')
    else
        TOTAL_RAM=8
    fi
    
    echo "$TOTAL_RAM"
}

# Main installation
print_header "KimiClaw Business OS Installation"
echo "Your AI. Your data. Your business."
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "Please do not run this script as root"
    exit 1
fi

# Detect OS
OS=$(detect_os)
print_success "Detected OS: $OS"

# Check RAM
RAM=$(check_ram)
print_success "Detected RAM: ${RAM}GB"

if [ "$RAM" -ge 16 ]; then
    MODE="full"
    print_success "System will run in FULL MODE (with vision AI)"
else
    MODE="lite"
    print_warning "System will run in LITE MODE (8GB RAM detected, vision AI disabled)"
fi

# Install system dependencies
print_header "Installing system dependencies..."

if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv postgresql redis-server curl git
    print_success "System dependencies installed"
    
elif [[ "$OS" == "macos" ]]; then
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        print_error "Homebrew not found. Please install from https://brew.sh"
        exit 1
    fi
    
    brew install python postgresql redis
    print_success "System dependencies installed"
else
    print_error "Unsupported operating system: $OS"
    exit 1
fi

# Install Ollama
print_header "Installing Ollama..."

if ! command -v ollama &> /dev/null; then
    if [[ "$OS" == "macos" ]]; then
        brew install ollama
    else
        curl -fsSL https://ollama.ai/install.sh | sh
    fi
    print_success "Ollama installed"
else
    print_success "Ollama already installed"
fi

# Start Ollama service
print_header "Starting Ollama service..."
if [[ "$OS" == "linux-gnu"* ]]; then
    sudo systemctl start ollama || ollama serve &
elif [[ "$OS" == "macos" ]]; then
    ollama serve &
fi
sleep 3
print_success "Ollama service started"

# Pull required models
print_header "Downloading AI models (this may take several minutes)..."

ollama pull llama3.2
print_success "Downloaded conversation model (llama3.2)"

ollama pull mistral
print_success "Downloaded reasoning model (mistral)"

ollama pull nomic-embed-text
print_success "Downloaded embedding model (nomic-embed-text)"

if [ "$MODE" == "full" ]; then
    ollama pull llava:13b
    print_success "Downloaded vision model (llava:13b)"
fi

# Create KimiClaw directory
print_header "Setting up KimiClaw..."

INSTALL_DIR="$HOME/kimiclaw"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Clone or download KimiClaw
if [ ! -d ".git" ]; then
    print_header "Downloading KimiClaw Business OS..."
    # TODO: Replace with actual repository
    git clone https://github.com/yourusername/kimiclaw.git .
fi

# Create Python virtual environment
print_header "Creating Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_header "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Python packages installed"

# Setup PostgreSQL database
print_header "Configuring database..."

if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
    sudo -u postgres psql -c "CREATE DATABASE kimiclaw;" 2>/dev/null || true
    sudo -u postgres psql -c "CREATE USER kimiclaw WITH PASSWORD 'kimiclaw';" 2>/dev/null || true
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE kimiclaw TO kimiclaw;" 2>/dev/null || true
elif [[ "$OS" == "macos" ]]; then
    createdb kimiclaw 2>/dev/null || true
fi

print_success "Database configured"

# Start Redis
print_header "Starting Redis..."
if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
    sudo systemctl start redis-server
elif [[ "$OS" == "macos" ]]; then
    brew services start redis
fi
print_success "Redis started"

# Run installation wizard
print_header "Running setup wizard..."
python -m kimiclaw.cli.main install

# Create systemd service (Linux only)
if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
    print_header "Creating system service..."
    
    SERVICE_FILE="/etc/systemd/system/kimiclaw.service"
    sudo bash -c "cat > $SERVICE_FILE" << EOF
[Unit]
Description=KimiClaw Business OS
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin"
ExecStart=$INSTALL_DIR/venv/bin/python -m kimiclaw.cli.main serve
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable kimiclaw
    sudo systemctl start kimiclaw
    
    print_success "System service created and started"
fi

# Installation complete
echo ""
print_header "Installation Complete! 🎉"
echo ""
echo "KimiClaw Business OS is now installed and running."
echo ""
echo "Commands:"
echo "  kimiclaw status     - Show system status"
echo "  kimiclaw leads      - Run lead generation"
echo "  kimiclaw config     - Show configuration"
echo "  kimiclaw serve      - Start the server"
echo ""
echo "Web Dashboard: http://localhost:8000/dashboard"
echo "API Documentation: http://localhost:8000/docs"
echo ""
print_success "Your AI business assistant is ready! 🐝"
