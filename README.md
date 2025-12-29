# Sagatoyai - AI-Powered Plush Toys Platform

**The First AI-Powered Plush Toy Platform in Sweden and EU**

Sagatoyai brings artificial intelligence to traditional plush toys, creating interactive companions that can talk, tell stories, answer questions, and engage with children through natural conversation.

🌐 **Live**: https://sagatoy.com

## ✅ Recent Achievements

- **VPS Deployed**: Backend running on secured VPS at sagatoy.com
- **SSH 2FA Security**: Two-factor authentication with Google Authenticator
- **SSL/TLS**: HTTPS with auto-renewing Let's Encrypt certificates
- **Swedish Stories**: 12 pre-generated Swedish children's stories (T-Rex, Kanin, Delfin series)
- **Multi-LLM Support**: Groq, Gemini, and Ollama fallback chain
- **Edge TTS**: Swedish and English voice synthesis optimized for children

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────────────────────────┐
│   Plush Toy     │     │         VPS (sagatoy.com)            │
│   ESP32-S3      │────▶│  Nginx ─▶ FastAPI ─▶ Redis           │
│   + Mic/Speaker │     │           │                          │
└─────────────────┘     │     ┌─────┴─────┐                    │
                        │     ▼           ▼                    │
                        │   Groq       Edge TTS                │
                        │   Gemini     (Swedish/English)       │
                        │   Whisper                            │
                        └──────────────────────────────────────┘
```

## 📦 Project Structure

```
Sagatoyai/
├── backend/                    # FastAPI backend
│   ├── src/sagatoyai/
│   │   ├── api/               # REST API endpoints
│   │   ├── models/            # Data models
│   │   └── services/          # STT, LLM, TTS services
│   ├── stories/               # Pre-generated Swedish stories
│   │   └── sv/
│   │       ├── trex/          # T-Rex Adventures (4 stories)
│   │       ├── kanin/         # Kanin and Friends (4 stories)
│   │       └── delfin/        # Delfin the Helper (4 stories)
│   ├── scripts/               # Utility scripts
│   └── tests/                 # Test suite
├── deploy/                    # Deployment scripts & configs
│   ├── sagatoy.service        # Systemd service
│   ├── nginx_config_sagatoy.conf
│   └── *.sh                   # Setup & security scripts
├── docs/                      # Documentation
└── .kiro/specs/               # Feature specifications
```

## 🚀 VPS Deployment

### Server Details

- **Domain**: sagatoy.com
- **SSH Port**: 1025 (non-standard for security)
- **User**: harvard
- **Security**: SSH key + 2FA (Google Authenticator)

### Quick Deploy

```bash
# SSH to VPS (requires 2FA code)
ssh -p 1025 harvard@94.72.141.71

# Navigate to project
cd /var/www/sagatoy

# Pull latest changes
git pull origin main

# Restart service
sudo systemctl restart sagatoy

# Check status
sudo systemctl status sagatoy
```

### Test Endpoints

```bash
# Health check
curl https://sagatoy.com/api/v1/health

# Get auth token
curl -X POST https://sagatoy.com/api/v1/auth/device \
  -H "Content-Type: application/json" \
  -d '{"device_id": "test-001", "device_secret": "secret"}'

# Test conversation (use token from above)
curl -X POST https://sagatoy.com/api/v1/conversation \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test-1", "audio_data": ""}'
```

## 🔐 VPS Security Setup

The VPS is hardened with multiple security layers:

### SSH + 2FA Configuration

1. SSH key authentication only (no passwords)
2. Google Authenticator 2FA required
3. Non-standard SSH port (1025)
4. Fail2Ban for brute-force protection

### Firewall (UFW)

```bash
# Only these ports are open:
- 1025/tcp (SSH)
- 80/tcp (HTTP → redirects to HTTPS)
- 443/tcp (HTTPS)
```

### SSL/TLS

- Let's Encrypt certificates
- Auto-renewal via Certbot
- TLS 1.3 only

## 🛠️ Local Development

```bash
# Clone
git clone https://github.com/bluehawana/Sagatoyai.git
cd Sagatoyai/backend

# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
uvicorn sagatoyai.main:app --reload

# Test
pytest -v
```

## 📖 Swedish Story Library

12 pre-generated stories for children (3-10 years):

| Series                | Stories                                  | Theme                 |
| --------------------- | ---------------------------------------- | --------------------- |
| **T-Rex Adventures**  | Stockholm, Gothenburg, Malmö, Copenhagen | Swedish geography     |
| **Kanin and Friends** | Forest, Lake, River, Sea                 | Friendship & teamwork |
| **Delfin the Helper** | Fishermen, Rescue, Swimming, Ocean       | Helping others        |

Generate new stories:

```bash
cd backend
python scripts/generate_stories.py --language sv --series all
```

## 📡 API Endpoints

| Endpoint               | Method | Description                 |
| ---------------------- | ------ | --------------------------- |
| `/api/v1/health`       | GET    | Health check                |
| `/api/v1/auth/device`  | POST   | Device authentication       |
| `/api/v1/conversation` | POST   | Voice conversation pipeline |
| `/api/v1/weather`      | GET    | Weather information         |

## 🔧 Environment Variables

```bash
# Required
SECRET_KEY=your-secret-key
GOOGLE_API_KEY=your-gemini-key

# Optional
GROQ_API_KEY=your-groq-key
OLLAMA_URL=http://localhost:11434
TTS_VOICE_SV=sv-SE-SofieNeural
TTS_VOICE_EN=en-US-JennyNeural
```

## 🌟 Roadmap

- [x] Backend API with JWT auth
- [x] STT (Whisper), LLM (Groq/Gemini), TTS (Edge)
- [x] VPS deployment with SSL
- [x] SSH 2FA security
- [x] Swedish story library (12 stories)
- [ ] Wire up full conversation pipeline
- [ ] ESP32 firmware
- [ ] Mobile app for parents
- [ ] Wake word detection

## 📄 License

Copyright © 2024 Sagatoyai Project. All rights reserved.

---

**Made with ❤️ in Sweden - Pioneering AI Toys in the EU**
