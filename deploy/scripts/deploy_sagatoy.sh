#!/bin/bash

################################################################################
# SagaToy Quick Deploy Script
#
# This script deploys the Sagatoyai application to your VPS
#
# Prerequisites:
# - VPS setup script already run (vps_setup_sagatoy.sh)
# - DNS configured (sagatoy.com → your-vps-ip)
# - .env file configured
#
# Usage: bash deploy_sagatoy.sh
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

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

clear
print_header "SagaToy Deployment"

APP_DIR="/var/www/sagatoy"

################################################################################
# 1. CHECK PREREQUISITES
################################################################################

print_header "Phase 1: Check Prerequisites"

# Check if running from app directory
if [ ! -f "backend/pyproject.toml" ]; then
    print_error "Please run this script from the Sagatoyai root directory"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    echo "Please create .env file based on .env.example"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | awk '{print $2}' | cut -d. -f1,2)
if (( $(echo "$PYTHON_VERSION < 3.9" | bc -l) )); then
    print_error "Python 3.9+ required. Found: $PYTHON_VERSION"
    exit 1
fi

print_success "Prerequisites check passed"

################################################################################
# 2. CREATE DIRECTORIES
################################################################################

print_header "Phase 2: Create Directories"

mkdir -p logs
mkdir -p static
mkdir -p data

print_success "Directories created"

################################################################################
# 3. PYTHON ENVIRONMENT
################################################################################

print_header "Phase 3: Python Environment"

if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

print_info "Activating virtual environment..."
source venv/bin/activate

print_info "Upgrading pip..."
pip install --upgrade pip --quiet

print_info "Installing dependencies..."
cd backend
pip install -e . --quiet

print_success "Dependencies installed"

################################################################################
# 4. TEST APPLICATION
################################################################################

print_header "Phase 4: Test Application"

print_info "Running tests..."
if pytest tests/ -v; then
    print_success "All tests passed"
else
    print_warning "Some tests failed, but continuing..."
fi

################################################################################
# 5. SYSTEMD SERVICE
################################################################################

print_header "Phase 5: Install Systemd Service"

if [ -f "../sagatoy.service" ]; then
    sudo cp ../sagatoy.service /etc/systemd/system/
    sudo systemctl daemon-reload
    print_success "Systemd service installed"
else
    print_warning "sagatoy.service file not found, skipping"
fi

################################################################################
# 6. NGINX CONFIGURATION
################################################################################

print_header "Phase 6: Configure Nginx"

if [ -f "../nginx_config_sagatoy.conf" ]; then
    # Copy nginx config
    sudo cp ../nginx_config_sagatoy.conf /etc/nginx/sites-available/sagatoy.com

    # Create symlink if not exists
    if [ ! -L "/etc/nginx/sites-enabled/sagatoy.com" ]; then
        sudo ln -s /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/
    fi

    # Test nginx config
    if sudo nginx -t; then
        print_success "Nginx configuration valid"
        sudo systemctl reload nginx
    else
        print_error "Nginx configuration has errors!"
        exit 1
    fi
else
    print_warning "nginx_config_sagatoy.conf not found, skipping"
fi

################################################################################
# 7. SSL CERTIFICATE
################################################################################

print_header "Phase 7: SSL Certificate"

if [ ! -d "/etc/letsencrypt/live/sagatoy.com" ]; then
    print_info "No SSL certificate found. Running Certbot..."
    echo ""
    print_warning "Make sure DNS is configured before continuing!"
    read -p "Continue with SSL setup? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo certbot --nginx -d sagatoy.com -d www.sagatoy.com
        print_success "SSL certificate installed"
    else
        print_warning "Skipping SSL setup. You can run it later with:"
        echo "  sudo certbot --nginx -d sagatoy.com -d www.sagatoy.com"
    fi
else
    print_success "SSL certificate already exists"
fi

################################################################################
# 8. START SERVICE
################################################################################

print_header "Phase 8: Start Service"

if systemctl is-active --quiet sagatoy; then
    print_info "Restarting service..."
    sudo systemctl restart sagatoy
else
    print_info "Starting service..."
    sudo systemctl enable sagatoy
    sudo systemctl start sagatoy
fi

# Wait a moment for service to start
sleep 3

if systemctl is-active --quiet sagatoy; then
    print_success "Service is running"
else
    print_error "Service failed to start!"
    echo "Check logs with: sudo journalctl -u sagatoy -n 50"
    exit 1
fi

################################################################################
# 9. VERIFY DEPLOYMENT
################################################################################

print_header "Phase 9: Verify Deployment"

# Test health endpoint
print_info "Testing health endpoint..."
if curl -sf http://localhost:8000/health > /dev/null; then
    print_success "Health endpoint responding"
else
    print_warning "Health endpoint not responding"
fi

# Check if HTTPS is available
if [ -d "/etc/letsencrypt/live/sagatoy.com" ]; then
    print_info "Testing HTTPS endpoint..."
    if curl -sf https://sagatoy.com/health > /dev/null; then
        print_success "HTTPS endpoint responding"
    else
        print_warning "HTTPS endpoint not responding yet (may need DNS propagation)"
    fi
fi

################################################################################
# COMPLETION
################################################################################

print_header "Deployment Complete!"

echo -e "${GREEN}${BOLD}✓ SagaToy is deployed!${NC}"
echo ""
echo -e "${BOLD}Service Status:${NC}"
sudo systemctl status sagatoy --no-pager | head -10
echo ""
echo -e "${BOLD}Quick Commands:${NC}"
echo "  View logs:     ${CYAN}sudo journalctl -u sagatoy -f${NC}"
echo "  Restart:       ${CYAN}sudo systemctl restart sagatoy${NC}"
echo "  Stop:          ${CYAN}sudo systemctl stop sagatoy${NC}"
echo "  Status:        ${CYAN}sudo systemctl status sagatoy${NC}"
echo ""
echo -e "${BOLD}Endpoints:${NC}"
echo "  Health:        ${CYAN}https://sagatoy.com/health${NC}"
echo "  API Docs:      ${CYAN}https://sagatoy.com/docs${NC}"
echo "  API:           ${CYAN}https://sagatoy.com/api${NC}"
echo ""
echo -e "${BOLD}Next Steps:${NC}"
echo "  1. Test API: curl https://sagatoy.com/health"
echo "  2. View docs: https://sagatoy.com/docs"
echo "  3. Configure device with API endpoint"
echo "  4. Monitor logs: sudo journalctl -u sagatoy -f"
echo ""
echo -e "${GREEN}Happy deploying! 🚀${NC}"
echo ""
