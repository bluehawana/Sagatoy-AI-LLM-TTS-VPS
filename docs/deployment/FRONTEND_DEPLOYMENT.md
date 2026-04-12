# Frontend Deployment Guide for Sagatoyai

This guide explains how to deploy the Next.js frontend alongside the FastAPI backend on your VPS at sagatoy.com.

## Architecture

```
                      ┌─────────────────────────────┐
                      │         sagatoy.com         │
                      │    (Nginx Port 443/80)      │
                      └──────────┬──────────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                 │
         ┌──────▼─────────┐            ┌────────▼────────┐
         │   Next.js      │            │   FastAPI       │
         │   Port 3000    │            │   Port 8000     │
         │   (Frontend)   │            │   (Backend)     │
         └────────────────┘            └─────────────────┘
```

## Prerequisites

1. Backend already deployed and running on port 8000
2. Node.js installed on VPS (v18 or higher)
3. Nginx configured with SSL/TLS
4. SSH access to VPS

## Deployment Steps

### 1. SSH to Your VPS

```bash
ssh -p 1025 harvard@94.72.141.71
# Enter your 2FA code when prompted
```

### 2. Navigate to Project Directory

```bash
cd /var/www/sagatoy
```

### 3. Pull Latest Changes

```bash
git pull origin main
```

### 4. Install Node.js (if not already installed)

```bash
# Check if Node.js is installed
node --version

# If not installed, install using NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

### 5. Deploy Frontend

```bash
cd /var/www/sagatoy
chmod +x deploy/deploy_frontend.sh
sudo deploy/deploy_frontend.sh
```

The script will:
- Install frontend dependencies
- Build the Next.js application
- Set up systemd service for frontend
- Update nginx configuration
- Restart all services

### 6. Verify Deployment

```bash
# Check frontend service
sudo systemctl status sagatoy-frontend

# Check backend service
sudo systemctl status sagatoy

# Check nginx
sudo systemctl status nginx

# Test endpoints
curl https://sagatoy.com/
curl https://sagatoy.com/api/v1/health
```

## Manual Deployment (Alternative)

If you prefer to deploy manually:

### Install Dependencies

```bash
cd /var/www/sagatoy/frontend
npm install --production
```

### Build Frontend

```bash
npm run build
```

### Set Up Service

```bash
sudo cp ../deploy/sagatoy-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sagatoy-frontend
sudo systemctl start sagatoy-frontend
```

### Update Nginx

```bash
sudo cp ../deploy/nginx_sagatoy_full.conf /etc/nginx/sites-available/sagatoy.com
sudo ln -sf /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Service Management

### Start/Stop Services

```bash
# Frontend
sudo systemctl start sagatoy-frontend
sudo systemctl stop sagatoy-frontend
sudo systemctl restart sagatoy-frontend

# Backend
sudo systemctl restart sagatoy
```

### View Logs

```bash
# Frontend logs
sudo journalctl -u sagatoy-frontend -f

# Backend logs
sudo journalctl -u sagatoy -f

# Nginx logs
sudo tail -f /var/log/nginx/sagatoy.com.access.log
sudo tail -f /var/log/nginx/sagatoy.com.error.log
```

## Updating the Frontend

When you make changes to the frontend:

```bash
cd /var/www/sagatoy
git pull origin main
cd frontend
npm install
npm run build
sudo systemctl restart sagatoy-frontend
```

## Troubleshooting

### Frontend Won't Start

```bash
# Check the logs
sudo journalctl -u sagatoy-frontend -n 50 --no-pager

# Check if port 3000 is already in use
sudo lsof -i :3000

# Verify Node.js installation
node --version
npm --version
```

### Nginx Issues

```bash
# Test nginx configuration
sudo nginx -t

# Check nginx error log
sudo tail -f /var/log/nginx/error.log

# Reload nginx
sudo systemctl reload nginx
```

### Port Conflicts

If port 3000 is already in use, update the service file:

```bash
sudo nano /etc/systemd/system/sagatoy-frontend.service
# Change PORT=3000 to PORT=3001

sudo nano /etc/nginx/sites-available/sagatoy.com
# Update upstream nextjs_frontend to use port 3001

sudo systemctl daemon-reload
sudo systemctl restart sagatoy-frontend
sudo systemctl reload nginx
```

## URLs After Deployment

- **Frontend (Main Website)**: https://sagatoy.com
- **Backend API**: https://sagatoy.com/api/v1/
- **API Health Check**: https://sagatoy.com/api/v1/health
- **API Documentation**: https://sagatoy.com/docs

## Security Notes

1. The frontend runs on port 3000 (localhost only)
2. The backend runs on port 8000 (localhost only)
3. Only nginx (443/80) and SSH (1025) are exposed externally
4. All traffic is encrypted with TLS 1.2/1.3
5. SSL certificates auto-renew via Certbot

## Performance Optimization

The nginx configuration includes:
- Static asset caching (60 minutes)
- Image optimization caching (24 hours)
- Gzip compression
- HTTP/2 support

## Monitoring

Monitor your services with:

```bash
# Real-time status
watch -n 5 'systemctl is-active sagatoy-frontend sagatoy nginx'

# Resource usage
htop

# Disk space
df -h
```
