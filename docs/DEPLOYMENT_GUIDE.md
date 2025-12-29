# SagaToy VPS Deployment Guide

Complete guide to deploy Sagatoyai FastAPI backend to your VPS at sagatoy.com

## 📋 Prerequisites

- ✅ VPS with 2FA security configured
- ✅ Domain: sagatoy.com (DNS configured)
- ✅ SSH access: `ssh -p 1025 harvard@your-vps-ip`
- ✅ API keys ready (OpenAI, Groq, Gemini, etc.)

## 🚀 Quick Deploy (5 Steps)

### Step 1: Install Required Software

**Upload and run the setup script:**

```bash
# From your local machine
scp -P 1025 vps_setup_sagatoy.sh harvard@your-vps-ip:/tmp/

# SSH to VPS
ssh -p 1025 harvard@your-vps-ip

# Run setup script
sudo bash /tmp/vps_setup_sagatoy.sh
```

**What it installs:**
- Python 3.11
- Redis
- Docker & Docker Compose
- Nginx
- Certbot (SSL)
- Git & build tools
- FFmpeg (for audio processing)

**Duration:** ~5-10 minutes

### Step 2: Configure DNS

**Point your domain to your VPS:**

```
A Record:     sagatoy.com         →  94.72.141.71
A Record:     www.sagatoy.com     →  94.72.141.71
```

**Wait for DNS propagation** (5-60 minutes)

**Verify DNS:**
```bash
nslookup sagatoy.com
# Should return your VPS IP
```

### Step 3: Clone Repository

```bash
cd /var/www/sagatoy
git clone https://github.com/bluehawana/Sagatoyai-LLM-TTS-VPS.git .

# Or if you prefer to keep it separate:
git clone https://github.com/bluehawana/Sagatoyai-LLM-TTS-VPS.git
mv Sagatoyai-LLM-TTS-VPS/* .
rm -rf Sagatoyai-LLM-TTS-VPS
```

### Step 4: Set Up Python Environment

```bash
cd /var/www/sagatoy

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
cd backend
pip install --upgrade pip
pip install -e .

# For production, also install production dependencies
pip install gunicorn uvloop httptools
```

### Step 5: Configure Environment Variables

**Create `.env` file:**

```bash
nano /var/www/sagatoy/.env
```

**Add your configuration (see `.env.example` below)**

### Step 6: Set Up Systemd Service

```bash
# Copy service file
sudo cp sagatoy.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable sagatoy

# Start service
sudo systemctl start sagatoy

# Check status
sudo systemctl status sagatoy
```

### Step 7: Configure Nginx

```bash
# Copy nginx configuration
sudo cp nginx_config_sagatoy.conf /etc/nginx/sites-available/sagatoy.com

# Create symlink
sudo ln -s /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### Step 8: Get SSL Certificate

```bash
# Run Certbot to get SSL certificate
sudo certbot --nginx -d sagatoy.com -d www.sagatoy.com

# Follow prompts:
# - Enter email
# - Agree to terms
# - Choose redirect HTTP to HTTPS (option 2)

# Test auto-renewal
sudo certbot renew --dry-run
```

### Step 9: Test Deployment

```bash
# Test health endpoint
curl https://sagatoy.com/health

# Test API docs
curl https://sagatoy.com/docs

# View logs
sudo journalctl -u sagatoy -f
```

## 📝 Environment Variables (.env)

Create `/var/www/sagatoy/.env` with:

```bash
# Application Settings
APP_NAME=Sagatoyai
APP_ENV=production
DEBUG=false
LOG_LEVEL=info

# Server Settings
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Security
SECRET_KEY=your-very-long-random-secret-key-here-generate-with-openssl
JWT_SECRET_KEY=another-different-secret-key-for-jwt
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
SESSION_EXPIRE_SECONDS=3600

# OpenAI API (for Whisper STT)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Groq API (for fast LLM)
GROQ_API_KEY=gsk_your-groq-api-key-here
GROQ_MODEL=llama-3.1-70b-versatile

# Google Gemini API (alternative LLM)
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-flash

# Ollama (local LLM - optional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# LLM Fallback Strategy
PRIMARY_LLM=groq
FALLBACK_LLM=gemini

# TTS Settings (Microsoft Edge TTS)
TTS_VOICE=sv-SE-SofieNeural
TTS_RATE=+0%
TTS_VOLUME=+0%

# Content Safety
ENABLE_CONTENT_FILTER=true
CHILD_SAFETY_MODE=strict

# Weather API
WEATHER_API_ENABLED=true

# CORS Settings
ALLOWED_ORIGINS=https://sagatoy.com,https://www.sagatoy.com
ALLOWED_METHODS=GET,POST,PUT,DELETE
ALLOWED_HEADERS=*

# Logging
LOG_FILE=/var/www/sagatoy/logs/sagatoy.log
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5
```

**Generate secret keys:**
```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Generate JWT_SECRET_KEY
openssl rand -hex 32
```

## 🔍 Verification Checklist

After deployment, verify:

```bash
# 1. Service is running
sudo systemctl status sagatoy
# Should show: Active: active (running)

# 2. Health endpoint responds
curl https://sagatoy.com/health
# Should return: {"status":"healthy"}

# 3. API docs accessible
curl -I https://sagatoy.com/docs
# Should return: 200 OK

# 4. Redis is working
redis-cli ping
# Should return: PONG

# 5. Nginx is serving HTTPS
curl -I https://sagatoy.com
# Should show: HTTP/2 200

# 6. SSL certificate is valid
openssl s_client -connect sagatoy.com:443 -servername sagatoy.com
# Check expiry date

# 7. Logs are working
sudo journalctl -u sagatoy -n 50
# Should show recent log entries

# 8. Firewall allows HTTPS
sudo ufw status | grep 443
# Should show: 443/tcp ALLOW
```

## 📊 Monitoring

### View Application Logs

```bash
# Follow logs in real-time
sudo journalctl -u sagatoy -f

# View last 100 lines
sudo journalctl -u sagatoy -n 100

# Filter by time
sudo journalctl -u sagatoy --since "1 hour ago"

# View errors only
sudo journalctl -u sagatoy -p err
```

### Check Application Status

```bash
# Service status
sudo systemctl status sagatoy

# Restart service
sudo systemctl restart sagatoy

# Stop service
sudo systemctl stop sagatoy

# Start service
sudo systemctl start sagatoy
```

### Monitor Resources

```bash
# CPU and memory usage
htop

# Disk usage
df -h

# Redis memory
redis-cli INFO memory

# Nginx status
sudo systemctl status nginx

# Active connections
sudo netstat -tunlp | grep :8000
```

## 🔄 Updates & Maintenance

### Deploy New Version

```bash
cd /var/www/sagatoy

# Pull latest code
git pull origin main

# Activate venv
source venv/bin/activate

# Install/update dependencies
cd backend
pip install -e .

# Restart service
sudo systemctl restart sagatoy

# Check logs
sudo journalctl -u sagatoy -f
```

### Database Migrations (if needed)

```bash
# If you add a database later
cd /var/www/sagatoy
source venv/bin/activate

# Run migrations
alembic upgrade head

# Restart service
sudo systemctl restart sagatoy
```

### Backup

```bash
# Backup environment file
sudo cp /var/www/sagatoy/.env /root/backups/.env.backup.$(date +%Y%m%d)

# Backup Redis data (if needed)
sudo redis-cli SAVE
sudo cp /var/lib/redis/dump.rdb /root/backups/redis.$(date +%Y%m%d).rdb

# Backup application code
tar -czf /root/backups/sagatoy.$(date +%Y%m%d).tar.gz /var/www/sagatoy
```

## 🆘 Troubleshooting

### Application won't start

```bash
# Check logs
sudo journalctl -u sagatoy -n 100

# Common issues:
# 1. Missing environment variables
cat /var/www/sagatoy/.env

# 2. Redis not running
sudo systemctl status redis-server
sudo systemctl start redis-server

# 3. Port already in use
sudo netstat -tunlp | grep :8000

# 4. Python dependencies missing
source /var/www/sagatoy/venv/bin/activate
pip install -e backend/
```

### SSL certificate issues

```bash
# Check certificate expiry
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

### Nginx errors

```bash
# Check nginx config
sudo nginx -t

# View nginx logs
sudo tail -100 /var/log/nginx/sagatoy.com.error.log

# Restart nginx
sudo systemctl restart nginx
```

### High CPU/Memory usage

```bash
# Check which process
htop

# Reduce workers in systemd service
sudo nano /etc/systemd/system/sagatoy.service
# Change --workers 4 to --workers 2

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart sagatoy
```

## 🔒 Security Checklist

- [x] 2FA enabled for SSH
- [x] Firewall (UFW) configured
- [x] Fail2Ban protecting SSH
- [x] SSL/TLS certificate installed
- [x] Strong secret keys in .env
- [x] Content filtering enabled
- [x] CORS configured properly
- [x] Regular security updates enabled

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Nginx Docs**: https://nginx.org/en/docs/
- **Certbot**: https://certbot.eff.org/
- **Redis**: https://redis.io/documentation
- **Systemd Services**: https://www.freedesktop.org/software/systemd/man/systemd.service.html

## 🎉 Success!

Once all steps are complete, your Sagatoyai backend will be:

✅ **Running**: https://sagatoy.com/health
✅ **Documented**: https://sagatoy.com/docs
✅ **Secure**: SSL/TLS + 2FA + Firewall
✅ **Monitored**: Systemd + Logs
✅ **Auto-restart**: On crash or reboot
✅ **Auto-update**: Security patches

**Your AI plush toy platform is live!** 🧸🤖
