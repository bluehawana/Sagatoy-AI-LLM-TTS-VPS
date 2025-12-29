# Deploy Sagatoy to VPS + Cloudflare - LIVE NOW

## Option 1: Deploy to VPS (Recommended for Full Control)

### Step 1: SSH to VPS
```bash
ssh -p 1025 harvard@94.72.141.71
# Enter your 2FA code
```

### Step 2: Install Node.js (if needed)
```bash
# Check if installed
node --version

# If not installed or version < 18:
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version  # Should be v20.x
npm --version
```

### Step 3: Deploy Frontend
```bash
# Navigate to project
cd /var/www/sagatoy

# Pull latest changes
git pull origin main

# Install and build frontend
cd frontend
npm install
npm run build

# Setup systemd service
sudo cp ../deploy/sagatoy-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sagatoy-frontend
sudo systemctl start sagatoy-frontend

# Check status
sudo systemctl status sagatoy-frontend
```

### Step 4: Configure Nginx
```bash
# Copy nginx config
sudo cp /var/www/sagatoy/deploy/nginx_sagatoy_full.conf /etc/nginx/sites-available/sagatoy.com

# Create/update symlink
sudo ln -sf /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### Step 5: Verify VPS Deployment
```bash
# Check services
sudo systemctl status sagatoy-frontend
sudo systemctl status nginx

# Test locally
curl http://localhost:3000

# Test with SSL
curl https://sagatoy.com
```

---

## Option 2: Deploy to Cloudflare Pages (Fastest)

### Step 1: Login to Cloudflare
1. Go to https://dash.cloudflare.com
2. Click "Pages" in the left sidebar
3. Click "Create a project"

### Step 2: Connect GitHub
1. Click "Connect to Git"
2. Select your GitHub account
3. Choose repository: `Sagatoy-AI-LLM-TTS-VPS`
4. Click "Begin setup"

### Step 3: Configure Build Settings
```
Project name: sagatoy
Production branch: main
Build command: cd frontend && npm run build
Build output directory: frontend/.next
Root directory: /
```

### Step 4: Environment Variables
Add these if needed (usually not required for static builds):
```
NODE_VERSION=20
```

### Step 5: Deploy
1. Click "Save and Deploy"
2. Wait 2-3 minutes for build to complete
3. You'll get a URL like: `sagatoy.pages.dev`

### Step 6: Custom Domain (sagatoy.com)
1. In Cloudflare Pages, go to your project
2. Click "Custom domains"
3. Click "Set up a custom domain"
4. Enter: `sagatoy.com` and `www.sagatoy.com`
5. Cloudflare will automatically configure DNS

---

## Option 3: Hybrid (VPS Backend + CF Frontend)

### Best of Both Worlds:
- **Cloudflare Pages**: Serves the frontend (fast, global CDN)
- **VPS**: Runs the backend API

### Setup:
1. Deploy frontend to Cloudflare Pages (see Option 2)
2. Keep backend running on VPS
3. Update API calls to point to: `https://api.sagatoy.com`

### DNS Configuration in Cloudflare:
```
Type    Name    Content             Proxy
A       @       94.72.141.71        Proxied (orange cloud)
CNAME   www     sagatoy.com         Proxied (orange cloud)
A       api     94.72.141.71        Proxied (orange cloud)
```

---

## Quick VPS One-Liner Deploy

```bash
ssh -p 1025 harvard@94.72.141.71 << 'ENDSSH'
cd /var/www/sagatoy && \
git pull origin main && \
cd frontend && \
npm install && \
npm run build && \
sudo systemctl restart sagatoy-frontend && \
sudo systemctl reload nginx && \
curl -I https://sagatoy.com
ENDSSH
```

---

## Cloudflare DNS Settings

Make sure these records exist in Cloudflare DNS:

```
Type    Name    Content             TTL     Proxy Status
A       @       94.72.141.71        Auto    Proxied
A       www     94.72.141.71        Auto    Proxied
CNAME   api     @                   Auto    Proxied
```

### Enable Cloudflare Features:
1. **SSL/TLS**: Set to "Full (strict)"
2. **Always Use HTTPS**: ON
3. **Auto Minify**: Enable HTML, CSS, JS
4. **Brotli**: ON
5. **Caching**: Standard

---

## Verification Steps

### Check VPS
```bash
curl -I https://sagatoy.com
curl https://sagatoy.com/api/v1/health
```

### Check DNS
```bash
dig sagatoy.com
nslookup sagatoy.com
```

### Check in Browser
1. https://sagatoy.com - Should show your landing page
2. https://www.sagatoy.com - Should redirect to sagatoy.com
3. Check SSL certificate - Should be valid

---

## Troubleshooting

### VPS: Port 3000 in use
```bash
sudo lsof -i :3000
sudo systemctl restart sagatoy-frontend
```

### VPS: Nginx errors
```bash
sudo nginx -t
sudo systemctl reload nginx
sudo tail -f /var/log/nginx/error.log
```

### Cloudflare: Build failed
- Check build logs in Cloudflare Pages dashboard
- Verify `package.json` has correct scripts
- Check Node.js version compatibility

### DNS not propagating
```bash
# Check current DNS
dig sagatoy.com @1.1.1.1

# Clear DNS cache (local)
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

---

## Recommended: VPS Deployment

For your use case (job application showing live backend + frontend):
- ✅ Deploy to VPS (full control, shows DevOps skills)
- ✅ Use Cloudflare for DNS and CDN (free tier)
- ✅ Keep backend on VPS at `/api` routes
- ✅ Shows you can manage full infrastructure

This demonstrates:
- Full-stack deployment
- Server management
- SSL/security
- Professional DevOps workflow
