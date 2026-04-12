#!/bin/bash
set -e

echo "================================================"
echo "Sagatoyai Frontend Deployment Script"
echo "================================================"

# Configuration
FRONTEND_DIR="/var/www/sagatoy/frontend"
SERVICE_FILE="sagatoy-frontend.service"
NGINX_CONFIG="nginx_sagatoy_full.conf"

echo ""
echo "Step 1: Installing frontend dependencies..."
cd "$FRONTEND_DIR"
npm install --production

echo ""
echo "Step 2: Building Next.js application..."
npm run build

echo ""
echo "Step 3: Setting up systemd service..."
sudo cp "$FRONTEND_DIR/../deploy/$SERVICE_FILE" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_FILE
sudo systemctl restart $SERVICE_FILE

echo ""
echo "Step 4: Updating nginx configuration..."
sudo cp "$FRONTEND_DIR/../deploy/$NGINX_CONFIG" /etc/nginx/sites-available/sagatoy.com
sudo ln -sf /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/

echo ""
echo "Step 5: Testing nginx configuration..."
sudo nginx -t

echo ""
echo "Step 6: Reloading nginx..."
sudo systemctl reload nginx

echo ""
echo "Step 7: Checking service status..."
sudo systemctl status $SERVICE_FILE --no-pager

echo ""
echo "================================================"
echo "Frontend deployment completed!"
echo "================================================"
echo ""
echo "Services:"
echo "  Frontend: systemctl status sagatoy-frontend"
echo "  Backend:  systemctl status sagatoy"
echo "  Nginx:    systemctl status nginx"
echo ""
echo "Logs:"
echo "  Frontend: journalctl -u sagatoy-frontend -f"
echo "  Backend:  journalctl -u sagatoy -f"
echo "  Nginx:    tail -f /var/log/nginx/sagatoy.com.{access,error}.log"
echo ""
echo "Website: https://sagatoy.com"
echo "API: https://sagatoy.com/api/v1/health"
echo ""
