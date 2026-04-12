# Deploy Frontend to sagatoy.com - URGENT

## Quick Deploy Steps

### 1. SSH to Your VPS
```bash
ssh -p 1025 harvard@94.72.141.71
# Enter your 2FA code
```

### 2. Pull Latest Changes
```bash
cd /var/www/sagatoy
git pull origin main
```

### 3. Install Node.js (if not installed)
```bash
# Check version
node --version

# If not installed or old version:
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 4. Build and Deploy Frontend
```bash
cd /var/www/sagatoy/frontend

# Install dependencies
npm install

# Build for production
npm run build

# Setup systemd service
sudo cp ../deploy/sagatoy-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sagatoy-frontend
sudo systemctl start sagatoy-frontend

# Check status
sudo systemctl status sagatoy-frontend
```

### 5. Update Nginx
```bash
# Copy new nginx config
sudo cp /var/www/sagatoy/deploy/nginx_sagatoy_full.conf /etc/nginx/sites-available/sagatoy.com

# Create symlink if not exists
sudo ln -sf /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### 6. Verify
```bash
# Check services
sudo systemctl status sagatoy-frontend
sudo systemctl status nginx

# Test from server
curl http://localhost:3000

# Test from outside
curl https://sagatoy.com
```

## Quick One-Liner Deploy

If everything is already set up:

```bash
cd /var/www/sagatoy && \
git pull origin main && \
cd frontend && \
npm install && \
npm run build && \
sudo systemctl restart sagatoy-frontend && \
sudo systemctl reload nginx && \
echo "✅ Deployed! Check https://sagatoy.com"
```

## Troubleshooting

### Port 3000 Already in Use
```bash
sudo lsof -i :3000
sudo kill -9 <PID>
sudo systemctl restart sagatoy-frontend
```

### Nginx Errors
```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

### Service Won't Start
```bash
sudo journalctl -u sagatoy-frontend -n 50 --no-pager
```

## DNS Note
Make sure sagatoy.com points to your VPS IP: 94.72.141.71

Check with:
```bash
dig sagatoy.com
nslookup sagatoy.com
```

## Site Will Be Live At
- https://sagatoy.com (main site - frontend)
- https://www.sagatoy.com (should redirect)
- https://sagatoy.com/api/v1/health (backend API)
- https://sagatoy.com/docs (API docs)
