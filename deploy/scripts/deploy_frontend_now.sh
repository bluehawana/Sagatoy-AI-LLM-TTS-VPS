#!/bin/bash

# Sagatoy Frontend Deployment Script
# Run this to deploy to VPS NOW

set -e

echo "========================================="
echo "🚀 Deploying Sagatoy Frontend to VPS"
echo "========================================="

VPS_USER="harvard"
VPS_HOST="94.72.141.71"
VPS_PORT="1025"
PROJECT_DIR="/var/www/sagatoy"

echo ""
echo "📡 Connecting to VPS..."
echo "Note: You'll need to enter your 2FA code"
echo ""

ssh -p $VPS_PORT $VPS_USER@$VPS_HOST << 'ENDSSH'
set -e

echo "✅ Connected to VPS"
echo ""

# Navigate to project
cd /var/www/sagatoy || { echo "❌ Project directory not found"; exit 1; }

echo "📥 Pulling latest code from GitHub..."
git pull origin main

echo ""
echo "📦 Installing Node.js (if needed)..."
if ! command -v node &> /dev/null || [[ $(node -v | cut -d'v' -f2 | cut -d'.' -f1) -lt 18 ]]; then
    echo "Installing Node.js 20.x..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    echo "✅ Node.js $(node -v) already installed"
fi

echo ""
echo "🔧 Building frontend..."
cd frontend
npm install
npm run build

echo ""
echo "⚙️  Setting up systemd service..."
sudo cp ../deploy/sagatoy-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sagatoy-frontend

echo ""
echo "🔄 Restarting frontend service..."
sudo systemctl restart sagatoy-frontend

echo ""
echo "🌐 Configuring nginx..."
sudo cp ../deploy/nginx_sagatoy_full.conf /etc/nginx/sites-available/sagatoy.com
sudo ln -sf /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/

echo ""
echo "✅ Testing nginx configuration..."
sudo nginx -t

echo ""
echo "🔄 Reloading nginx..."
sudo systemctl reload nginx

echo ""
echo "========================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "========================================="
echo ""
echo "📊 Service Status:"
sudo systemctl status sagatoy-frontend --no-pager -l | head -15
echo ""
echo "🌍 Your site should now be live at:"
echo "   👉 https://sagatoy.com"
echo "   👉 https://www.sagatoy.com"
echo ""
echo "🔍 Testing connection..."
curl -I https://sagatoy.com 2>/dev/null | head -5 || echo "Note: May take a few seconds to propagate"

ENDSSH

echo ""
echo "========================================="
echo "🎉 Deployment script finished!"
echo "========================================="
echo ""
echo "🔗 Check your site: https://sagatoy.com"
echo ""
