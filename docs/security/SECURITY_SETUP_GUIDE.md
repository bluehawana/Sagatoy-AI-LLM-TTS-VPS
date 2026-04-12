# Complete Security & SSL Setup Guide for SagaToy VPS

**VPS**: Ubuntu 22.04 at 94.72.141.71
**Domain**: sagatoy.com
**Goal**: Maximum security with 2FA, SSL, and protection against attacks

---

## 🚨 CRITICAL: Security Setup Order

Follow these steps **in order**. Do NOT skip steps or log out before testing!

---

## PART 1: Initial Connection & Basic Security

### Step 1: Connect to Your VPS

```bash
ssh root@94.72.141.71
# OR
ssh yourusername@94.72.141.71
```

### Step 2: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 3: Create a New Admin User (if using root)

**NEVER use root directly. Create your own user:**

```bash
# Create new user (replace 'sagatoy' with your preferred username)
adduser sagatoy

# Add to sudo group
usermod -aG sudo sagatoy

# Test the new user (OPEN NEW TERMINAL, don't close root session yet!)
# In new terminal:
ssh sagatoy@94.72.141.71
sudo whoami    # Should output: root

# If it works, you can continue. Keep both terminals open!
```

---

## PART 2: Maximum Security Configuration

### Step 4: Install Security Packages

```bash
sudo apt install -y ufw fail2ban libpam-google-authenticator \
    openssh-server qrencode unattended-upgrades nginx \
    certbot python3-certbot-nginx
```

### Step 5: Configure Automatic Security Updates

```bash
sudo dpkg-reconfigure -plow unattended-upgrades
# Select "Yes" when prompted
```

### Step 6: Set Up Firewall (UFW)

```bash
# Reset firewall
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (port 22 for now)
sudo ufw allow 22/tcp

# Allow web traffic
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw --force enable

# Check status
sudo ufw status verbose
```

### Step 7: Configure Fail2ban (Auto-Block Attackers)

```bash
sudo tee /etc/fail2ban/jail.local > /dev/null <<'EOF'
[DEFAULT]
bantime = 86400
findtime = 600
maxretry = 3
destemail = admin@sagatoy.com
action = %(action_mwl)s

[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 86400

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

[nginx-badbots]
enabled = true
port = http,https
filter = nginx-badbots
logpath = /var/log/nginx/access.log
maxretry = 2
bantime = 86400
EOF

# Start fail2ban
sudo systemctl enable fail2ban
sudo systemctl restart fail2ban

# Check status
sudo fail2ban-client status
```

---

## PART 3: Two-Factor Authentication (2FA)

### Step 8: Install Google Authenticator App

**On your phone:**
- Download "Google Authenticator" from App Store or Google Play
- Open the app

### Step 9: Set Up 2FA for SSH

**Run as your regular user (NOT root):**

```bash
# Run as your user (e.g., sagatoy)
google-authenticator
```

**Answer the questions:**
1. "Do you want authentication tokens to be time-based?" → **Y** (Yes)
2. A **QR code** will appear → **Scan it with Google Authenticator app**
3. Save your emergency scratch codes somewhere safe!
4. "Do you want me to update your ~/.google_authenticator file?" → **Y**
5. "Do you want to disallow multiple uses?" → **Y**
6. "Do you want to increase time skew?" → **N**
7. "Do you want to enable rate-limiting?" → **Y**

### Step 10: Enable 2FA in SSH

```bash
# Edit PAM config
sudo nano /etc/pam.d/sshd
```

**Add this line at the TOP:**
```
auth required pam_google_authenticator.so nullok
```

**Comment out this line (add # at the beginning):**
```
#@include common-auth
```

Save and exit (Ctrl+X, Y, Enter)

```bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config
```

**Find and modify these lines:**
```
ChallengeResponseAuthentication yes
UsePAM yes
```

**Restart SSH (KEEP YOUR CURRENT SESSIONS OPEN!):**
```bash
sudo systemctl restart sshd
```

### Step 11: TEST 2FA (CRITICAL!)

**Open a NEW terminal (keep old one open!):**
```bash
ssh sagatoy@94.72.141.71
# You should now be asked for:
# 1. Password
# 2. Verification code (from Google Authenticator app)
```

**✅ If it works, great!**
**❌ If it doesn't work, you still have your old session open to fix it**

---

## PART 4: SSH Key Authentication (Even More Secure)

### Step 12: Generate SSH Key on Your Local Computer

**On your Windows computer (local machine, not VPS):**

```bash
# Open Git Bash or PowerShell
ssh-keygen -t ed25519 -C "sagatoy-vps-key"

# Press Enter to save to default location
# Enter a strong passphrase (optional but recommended)
```

### Step 13: Copy SSH Key to VPS

```bash
# Copy public key to VPS
ssh-copy-id sagatoy@94.72.141.71

# You'll be asked for password + 2FA code
```

### Step 14: Test SSH Key Login

**Open NEW terminal:**
```bash
ssh sagatoy@94.72.141.71
# Should only ask for 2FA code (not password)
```

### Step 15: Disable Password Authentication (SSH Keys Only)

**Only do this AFTER confirming SSH key works!**

```bash
sudo nano /etc/ssh/sshd_config
```

**Find and set:**
```
PasswordAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```

**Restart SSH:**
```bash
sudo systemctl restart sshd
```

---

## PART 5: Harden SSH Further

### Step 16: Change SSH Port (Optional but Recommended)

**This makes it harder for attackers to find your SSH:**

```bash
sudo nano /etc/ssh/sshd_config
```

**Find and change:**
```
Port 2222
# Or any port between 1024-65535
```

**Update firewall:**
```bash
sudo ufw allow 2222/tcp
sudo ufw delete allow 22/tcp
sudo ufw reload
```

**Restart SSH:**
```bash
sudo systemctl restart sshd
```

**Test in NEW terminal:**
```bash
ssh -p 2222 sagatoy@94.72.141.71
```

### Step 17: Disable Root Login

```bash
sudo nano /etc/ssh/sshd_config
```

**Set:**
```
PermitRootLogin no
```

**Restart:**
```bash
sudo systemctl restart sshd
```

---

## PART 6: SSL Certificate & Website Setup

### Step 18: Verify DNS is Configured

```bash
# On your VPS, check if DNS points to your server
nslookup sagatoy.com
nslookup www.sagatoy.com

# Both should show: 94.72.141.71
```

### Step 19: Create Website Directory

```bash
sudo mkdir -p /var/www/sagatoy.com
sudo chown -R www-data:www-data /var/www/sagatoy.com
sudo chmod -R 755 /var/www/sagatoy.com
```

### Step 20: Create Homepage

```bash
sudo tee /var/www/sagatoy.com/index.html > /dev/null <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SagaToy - Secure</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
        }
        .container {
            padding: 60px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
        }
        h1 { font-size: 4em; margin-bottom: 20px; }
        .badge {
            display: inline-block;
            background: #10b981;
            padding: 10px 20px;
            border-radius: 50px;
            margin: 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ SagaToy</h1>
        <p style="font-size: 1.5em; color: #4ade80;">✓ Secure & Protected</p>
        <div style="margin-top: 30px;">
            <span class="badge">🔐 2FA</span>
            <span class="badge">🔒 SSL/TLS</span>
            <span class="badge">🛡️ Firewall</span>
            <span class="badge">🚫 Fail2ban</span>
        </div>
    </div>
</body>
</html>
EOF
```

### Step 21: Configure Nginx

```bash
sudo tee /etc/nginx/sites-available/sagatoy.com > /dev/null <<'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name sagatoy.com www.sagatoy.com;

    root /var/www/sagatoy.com;
    index index.html;

    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    server_tokens off;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# If OK, restart
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### Step 22: Get SSL Certificate (Let's Encrypt)

```bash
sudo certbot --nginx \
    -d sagatoy.com \
    -d www.sagatoy.com \
    --email admin@sagatoy.com \
    --agree-tos \
    --redirect \
    --hsts

# Answer prompts:
# - Email: admin@sagatoy.com
# - Agree to terms: Y
# - Share email: N (optional)
```

### Step 23: Enable Auto-Renewal

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Test renewal
sudo certbot renew --dry-run
```

### Step 24: Verify SSL

```bash
# Check certificate
sudo certbot certificates

# Visit your site
# https://sagatoy.com
```

---

## PART 7: Cloudflare Configuration

### Step 25: Configure Cloudflare SSL/TLS

1. **Log into Cloudflare** → Select sagatoy.com
2. **Go to SSL/TLS** → Overview
3. **Set encryption mode**: **"Full (strict)"**
4. **Go to SSL/TLS** → Edge Certificates
   - Enable "Always Use HTTPS": ✅
   - Enable "Automatic HTTPS Rewrites": ✅
   - Minimum TLS Version: **TLS 1.2**
   - Enable "HSTS": ✅
     - Max Age: 6 months
     - Include subdomains: ✅
     - Preload: ✅

### Step 26: Enable Cloudflare Proxy (DDoS Protection)

1. **Go to DNS** → Records
2. **Find your A records**:
   - `sagatoy.com` → 94.72.141.71
   - `www.sagatoy.com` → 94.72.141.71
3. **Click the cloud icon** to turn it **ORANGE** (Proxied)
   - This hides your real IP and provides DDoS protection

### Step 27: Additional Cloudflare Security

**Security** → Settings:
- Security Level: **Medium** or **High**
- Challenge Passage: **30 minutes**
- Browser Integrity Check: ✅

**Firewall Rules** (optional):
- Create rule to block certain countries
- Create rule to block common attacks

---

## PART 8: Final Security Checks

### Step 28: Security Status Commands

Create a monitoring script:

```bash
sudo tee /usr/local/bin/security-status > /dev/null <<'EOF'
#!/bin/bash
echo "=== SECURITY STATUS ==="
echo ""
echo "Firewall Status:"
sudo ufw status numbered
echo ""
echo "Fail2ban Status:"
sudo fail2ban-client status
echo ""
echo "Banned IPs (SSH):"
sudo fail2ban-client status sshd
echo ""
echo "Active Connections:"
who
echo ""
echo "Recent Failed Logins:"
grep "Failed password" /var/log/auth.log | tail -10
echo ""
echo "SSL Certificate Expiry:"
sudo certbot certificates
echo ""
echo "Nginx Status:"
sudo systemctl status nginx --no-pager
EOF

sudo chmod +x /usr/local/bin/security-status

# Run it
security-status
```

### Step 29: Change Your Password

```bash
passwd
# Enter a STRONG password (20+ characters, mix of everything)
```

---

## 📋 SECURITY CHECKLIST

After completing all steps, verify:

- [ ] ✅ System updated
- [ ] ✅ Firewall (UFW) enabled and configured
- [ ] ✅ Fail2ban running
- [ ] ✅ 2FA enabled and working
- [ ] ✅ SSH keys configured
- [ ] ✅ Password authentication disabled
- [ ] ✅ Root login disabled
- [ ] ✅ SSH port changed (optional)
- [ ] ✅ Nginx running
- [ ] ✅ SSL certificate installed
- [ ] ✅ SSL auto-renewal enabled
- [ ] ✅ Cloudflare proxy enabled (orange cloud)
- [ ] ✅ Cloudflare SSL set to "Full (strict)"
- [ ] ✅ Strong user password set
- [ ] ✅ Emergency access method documented

---

## 🔐 How to Connect Now

**With custom SSH port (e.g., 2222):**
```bash
ssh -p 2222 sagatoy@94.72.141.71
```

**You'll need:**
1. Your SSH key passphrase (if you set one)
2. 2FA code from Google Authenticator app

---

## 🚨 EMERGENCY: Locked Out?

If you get locked out:
1. Use your VPS provider's **web console** (VNC)
2. Log in through the console
3. Fix SSH configuration:
   ```bash
   sudo nano /etc/ssh/sshd_config
   # Temporarily enable PasswordAuthentication yes
   sudo systemctl restart sshd
   ```

---

## 📊 Monitoring Commands

```bash
# Check security status
security-status

# Check firewall
sudo ufw status verbose

# Check fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd

# Unban an IP (if you accidentally banned yourself)
sudo fail2ban-client set sshd unbanip YOUR_IP

# Check SSL certificate
sudo certbot certificates

# View recent logins
last -20

# Check who's logged in
who

# Check system logs
sudo journalctl -xe
```

---

## 🎯 Your Site is Ready!

**Website**: https://sagatoy.com
**Admin**: 2FA-protected SSH access only
**Security**: Maximum

Your VPS is now **locked down** and protected against:
- ✅ Brute force attacks
- ✅ Unauthorized access
- ✅ DDoS attacks (via Cloudflare)
- ✅ Common exploits
- ✅ Port scanning
- ✅ Malicious bots

---

## Need Help?

If you get stuck at any step, note which step number and what error you're seeing.
