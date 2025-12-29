# SagaToy VPS Setup - Quick Reference

## 🎯 What We're Deploying

**Sagatoyai Backend** - FastAPI application for AI-powered plush toys
- **Tech Stack**: Python 3.11 + FastAPI + Redis + Nginx
- **Domain**: sagatoy.com
- **Services**: STT (Whisper), LLM (Groq/Gemini), TTS (Edge-TTS)

## 📁 Files Created

| File | Purpose |
|------|---------|
| `vps_setup_sagatoy.sh` | Install all required software (Python, Redis, Docker, Nginx, Certbot) |
| `nginx_config_sagatoy.conf` | Nginx reverse proxy configuration |
| `sagatoy.service` | Systemd service for auto-start/restart |
| `deploy_sagatoy.sh` | One-command deployment script |
| `.env.example` | Environment variables template |
| `DEPLOYMENT_GUIDE.md` | Complete step-by-step deployment guide |

## 🚀 Quick Start (3 Commands)

### 1. Upload Files to VPS

```bash
# From Windows PowerShell
scp -P 1025 vps_setup_sagatoy.sh nginx_config_sagatoy.conf sagatoy.service deploy_sagatoy.sh .env.example harvard@94.72.141.71:/tmp/
```

### 2. Run VPS Setup

```bash
# SSH to VPS
ssh -p 1025 harvard@94.72.141.71

# Run setup script
sudo bash /tmp/vps_setup_sagatoy.sh
```

**This installs:**
- ✅ Python 3.11
- ✅ Redis
- ✅ Docker & Docker Compose
- ✅ Nginx
- ✅ Certbot (SSL)
- ✅ Git & build tools

### 3. Deploy Application

```bash
# Move to app directory
cd /var/www/sagatoy

# Copy deployment files
cp /tmp/nginx_config_sagatoy.conf .
cp /tmp/sagatoy.service .
cp /tmp/deploy_sagatoy.sh .
cp /tmp/.env.example .env

# Edit .env with your API keys
nano .env

# Clone your repository
git clone https://github.com/bluehawana/Sagatoyai-LLM-TTS-VPS.git .

# Run deployment
bash deploy_sagatoy.sh
```

## 🔑 Required API Keys

Before deployment, get these API keys:

1. **OpenAI** (for Whisper STT)
   - Get at: https://platform.openai.com/api-keys
   - Set as: `OPENAI_API_KEY`

2. **Groq** (for fast LLM)
   - Get at: https://console.groq.com/keys
   - Set as: `GROQ_API_KEY`

3. **Google Gemini** (fallback LLM)
   - Get at: https://makersuite.google.com/app/apikey
   - Set as: `GEMINI_API_KEY`

## 📋 DNS Configuration

**Before SSL setup, configure DNS:**

```
Type    Name               Value           TTL
A       sagatoy.com        94.72.141.71    Auto
A       www.sagatoy.com    94.72.141.71    Auto
```

**Verify DNS propagation:**
```bash
nslookup sagatoy.com
# Should return: 94.72.141.71
```

## 🔒 Environment Variables

**Critical settings in `.env`:**

```bash
# Generate secret keys
openssl rand -hex 32  # For SECRET_KEY
openssl rand -hex 32  # For JWT_SECRET_KEY

# API Keys
OPENAI_API_KEY=sk-your-key
GROQ_API_KEY=gsk_your-key
GEMINI_API_KEY=your-key

# Domain
ALLOWED_ORIGINS=https://sagatoy.com,https://www.sagatoy.com
```

## 🎯 Deployment Steps

### Step 1: VPS Setup (10 minutes)
```bash
sudo bash vps_setup_sagatoy.sh
```

### Step 2: Configure DNS (5-60 minutes)
Wait for DNS propagation to complete.

### Step 3: Clone Repository
```bash
cd /var/www/sagatoy
git clone https://github.com/bluehawana/Sagatoyai-LLM-TTS-VPS.git .
```

### Step 4: Configure Environment
```bash
cp .env.example .env
nano .env  # Add your API keys
```

### Step 5: Deploy
```bash
bash deploy_sagatoy.sh
```

### Step 6: Get SSL Certificate
```bash
sudo certbot --nginx -d sagatoy.com -d www.sagatoy.com
```

## ✅ Verification

**After deployment, test:**

```bash
# 1. Health check
curl https://sagatoy.com/health
# Expected: {"status":"healthy"}

# 2. API docs
https://sagatoy.com/docs
# Should open Swagger UI

# 3. Service status
sudo systemctl status sagatoy
# Expected: Active: active (running)

# 4. View logs
sudo journalctl -u sagatoy -f
# Should show application logs
```

## 🔧 Common Commands

```bash
# View logs (follow)
sudo journalctl -u sagatoy -f

# Restart service
sudo systemctl restart sagatoy

# Check status
sudo systemctl status sagatoy

# Test nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx

# Check SSL certificate
sudo certbot certificates

# Renew SSL
sudo certbot renew
```

## 📊 Architecture

```
Internet
   ↓
UFW Firewall (ports 1025, 80, 443)
   ↓
Nginx (port 443 - HTTPS)
   ↓ reverse proxy
FastAPI (port 8000)
   ↓
Redis (port 6379 - sessions)
```

## 🔐 Security Features

- ✅ SSH 2FA enabled
- ✅ Firewall (UFW) configured
- ✅ Fail2Ban protecting SSH
- ✅ SSL/TLS (HTTPS only)
- ✅ Content filtering for children
- ✅ CORS properly configured
- ✅ Secret keys for JWT
- ✅ Environment variables protected

## 📈 Performance

**Recommended VPS specs:**
- **CPU**: 2+ cores
- **RAM**: 2GB+ (4GB recommended)
- **Storage**: 20GB+ SSD
- **Bandwidth**: 1TB+

**Current configuration:**
- **Workers**: 4 (adjustable in sagatoy.service)
- **Timeout**: 300s for LLM processing
- **Max upload**: 10MB (for audio files)

## 🚨 Troubleshooting

### Service won't start
```bash
# Check logs
sudo journalctl -u sagatoy -n 100

# Test manually
cd /var/www/sagatoy
source venv/bin/activate
uvicorn totoyai.main:app --host 0.0.0.0 --port 8000
```

### SSL certificate issues
```bash
# Check certificate
sudo certbot certificates

# Renew
sudo certbot renew --dry-run
```

### Redis not working
```bash
# Check Redis
sudo systemctl status redis-server

# Test connection
redis-cli ping
```

## 📝 Update Procedure

```bash
cd /var/www/sagatoy

# Pull latest code
git pull origin main

# Activate venv
source venv/bin/activate

# Update dependencies
cd backend
pip install -e .

# Restart service
sudo systemctl restart sagatoy

# Check logs
sudo journalctl -u sagatoy -f
```

## 🎉 Success Indicators

When everything is working:

✅ `https://sagatoy.com/health` returns `{"status":"healthy"}`
✅ `https://sagatoy.com/docs` shows Swagger UI
✅ `sudo systemctl status sagatoy` shows `Active: active (running)`
✅ `sudo journalctl -u sagatoy -f` shows activity logs
✅ SSL Labs gives A+ rating
✅ No errors in logs

## 📞 Support Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Deployment Guide**: See `DEPLOYMENT_GUIDE.md`
- **Project README**: See `README.md`
- **VPS Security**: See `VPS_SECURITY_README.md`

---

**Your AI plush toy platform is ready to go! 🧸🤖**

**Next**: Configure your ESP32 devices to connect to `https://sagatoy.com/api`
