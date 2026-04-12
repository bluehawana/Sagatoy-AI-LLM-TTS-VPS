#!/bin/bash

################################################################################
# SagaToy VPS Setup Script
#
# This script sets up your VPS for deploying the Sagatoyai FastAPI backend
#
# Requirements:
# - Ubuntu 22.04/24.04 LTS
# - Run as root: sudo bash vps_setup_sagatoy.sh
#
# What it installs:
# - Python 3.11
# - Redis
# - Docker & Docker Compose
# - Nginx
# - Certbot (for SSL)
# - Git
# - Required Python packages
#
################################################################################

set -e  # Exit on error

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

print_header() {
    echo ""
    echo -e "${CYAN}${BOLD}========================================${NC}"
    echo -e "${CYAN}${BOLD}$1${NC}"
    echo -e "${CYAN}${BOLD}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root: sudo bash $0"
    exit 1
fi

clear
print_header "SagaToy VPS Setup"

echo -e "${BOLD}This script will install:${NC}"
echo "  • Python 3.11"
echo "  • Redis (session storage)"
echo "  • Docker & Docker Compose"
echo "  • Nginx (reverse proxy)"
echo "  • Certbot (SSL certificates)"
echo "  • Git & build tools"
echo ""

read -p "Continue? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

################################################################################
# 1. SYSTEM UPDATE
################################################################################

print_header "Phase 1: System Update"

print_info "Updating package lists..."
apt update

print_info "Upgrading installed packages..."
apt upgrade -y

print_success "System updated"

################################################################################
# 2. INSTALL PYTHON 3.11
################################################################################

print_header "Phase 2: Install Python 3.11"

if python3.11 --version &>/dev/null; then
    print_success "Python 3.11 already installed"
else
    print_info "Installing Python 3.11..."
    apt install -y software-properties-common
    add-apt-repository -y ppa:deadsnakes/ppa
    apt update
    apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
    print_success "Python 3.11 installed"
fi

# Set Python 3.11 as default
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Verify
python3 --version
print_success "Python version: $(python3 --version)"

################################################################################
# 3. INSTALL REDIS
################################################################################

print_header "Phase 3: Install Redis"

if systemctl is-active --quiet redis-server; then
    print_success "Redis already installed and running"
else
    print_info "Installing Redis..."
    apt install -y redis-server

    # Configure Redis to start on boot
    systemctl enable redis-server
    systemctl start redis-server

    print_success "Redis installed and running"
fi

# Test Redis
if redis-cli ping | grep -q "PONG"; then
    print_success "Redis is responding"
else
    print_warning "Redis may not be working correctly"
fi

################################################################################
# 4. INSTALL DOCKER
################################################################################

print_header "Phase 4: Install Docker & Docker Compose"

if docker --version &>/dev/null; then
    print_success "Docker already installed"
else
    print_info "Installing Docker..."

    # Install prerequisites
    apt install -y ca-certificates curl gnupg lsb-release

    # Add Docker GPG key
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg

    # Add Docker repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Install Docker
    apt update
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Start Docker
    systemctl enable docker
    systemctl start docker

    print_success "Docker installed"
fi

# Verify
docker --version
docker compose version
print_success "Docker version: $(docker --version)"

################################################################################
# 5. INSTALL NGINX
################################################################################

print_header "Phase 5: Install Nginx"

if systemctl is-active --quiet nginx; then
    print_success "Nginx already installed and running"
else
    print_info "Installing Nginx..."
    apt install -y nginx

    systemctl enable nginx
    systemctl start nginx

    print_success "Nginx installed and running"
fi

nginx -v
print_success "Nginx version: $(nginx -v 2>&1)"

################################################################################
# 6. INSTALL CERTBOT
################################################################################

print_header "Phase 6: Install Certbot"

if certbot --version &>/dev/null; then
    print_success "Certbot already installed"
else
    print_info "Installing Certbot..."
    apt install -y certbot python3-certbot-nginx
    print_success "Certbot installed"
fi

certbot --version
print_success "Certbot version: $(certbot --version 2>&1 | head -1)"

################################################################################
# 7. INSTALL GIT & BUILD TOOLS
################################################################################

print_header "Phase 7: Install Git & Build Tools"

apt install -y git build-essential libssl-dev libffi-dev python3-dev

print_success "Git version: $(git --version)"

################################################################################
# 8. CREATE APPLICATION DIRECTORY
################################################################################

print_header "Phase 8: Create Application Directory"

APP_DIR="/var/www/sagatoy"

if [ -d "$APP_DIR" ]; then
    print_warning "Application directory already exists: $APP_DIR"
else
    mkdir -p "$APP_DIR"
    print_success "Created application directory: $APP_DIR"
fi

# Set ownership
chown -R $SUDO_USER:$SUDO_USER "$APP_DIR" 2>/dev/null || chown -R harvard:harvard "$APP_DIR"

################################################################################
# 9. INSTALL ADDITIONAL SYSTEM DEPENDENCIES
################################################################################

print_header "Phase 9: Install Additional Dependencies"

print_info "Installing audio and ML dependencies..."

# FFmpeg for audio processing (used by Whisper)
apt install -y ffmpeg

# Additional Python packages for ML
apt install -y python3-numpy python3-scipy

print_success "Additional dependencies installed"

################################################################################
# 10. CONFIGURE SYSTEM LIMITS
################################################################################

print_header "Phase 10: Configure System Limits"

print_info "Increasing file descriptor limits for production..."

# Add limits for better performance
cat >> /etc/security/limits.conf << 'EOF'

# SagaToy/Sagatoyai limits
* soft nofile 65536
* hard nofile 65536
* soft nproc 65536
* hard nproc 65536
EOF

print_success "System limits configured"

################################################################################
# COMPLETION
################################################################################

print_header "Installation Complete!"

echo -e "${GREEN}${BOLD}✓ VPS is ready for SagaToy deployment!${NC}"
echo ""
echo -e "${BOLD}Installed software:${NC}"
echo "  ✓ Python $(python3 --version 2>&1 | awk '{print $2}')"
echo "  ✓ Redis $(redis-server --version | awk '{print $3}')"
echo "  ✓ Docker $(docker --version | awk '{print $3}' | tr -d ',')"
echo "  ✓ Nginx $(nginx -v 2>&1 | awk '{print $3}')"
echo "  ✓ Certbot $(certbot --version 2>&1 | awk '{print $2}')"
echo "  ✓ Git $(git --version | awk '{print $3}')"
echo "  ✓ FFmpeg $(ffmpeg -version 2>&1 | head -1 | awk '{print $3}')"
echo ""
echo -e "${BOLD}Application directory:${NC} $APP_DIR"
echo ""
echo -e "${YELLOW}${BOLD}Next steps:${NC}"
echo ""
echo "1. Configure your domain DNS:"
echo "   Point sagatoy.com A record to: $(curl -s ifconfig.me)"
echo ""
echo "2. Clone your repository:"
echo "   cd $APP_DIR"
echo "   git clone https://github.com/yourusername/Sagatoyai-LLM-TTS-VPS.git ."
echo ""
echo "3. Set up environment variables:"
echo "   See: deployment_guide.md"
echo ""
echo "4. Install Python dependencies:"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -e backend/"
echo ""
echo "5. Configure Nginx and SSL:"
echo "   See: nginx_config_sagatoy.conf"
echo ""
echo -e "${GREEN}VPS setup complete! 🚀${NC}"
echo ""
