#!/bin/bash
# Secure SSL Setup Script for sagatoy.com
# This script implements strong security measures to prevent compromise
# Run as: sudo bash secure_ssl_setup.sh

set -e

echo "========================================="
echo "  SECURE SSL SETUP FOR SAGATOY.COM"
echo "  This includes hardened security config"
echo "========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root (use sudo)${NC}"
   exit 1
fi

echo -e "${GREEN}[1/12] Updating system packages...${NC}"
apt update && apt upgrade -y

echo -e "${GREEN}[2/12] Installing required packages...${NC}"
apt install -y nginx certbot python3-certbot-nginx ufw fail2ban git curl wget unattended-upgrades

echo -e "${GREEN}[3/12] Configuring automatic security updates...${NC}"
dpkg-reconfigure -plow unattended-upgrades

echo -e "${GREEN}[4/12] Hardening SSH configuration...${NC}"
# Backup original SSH config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Harden SSH
cat > /etc/ssh/sshd_config.d/hardening.conf <<'EOF'
# SSH Hardening Configuration
PermitRootLogin no
PasswordAuthentication yes
PubkeyAuthentication yes
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no
PrintMotd no
AcceptEnv LANG LC_*
MaxAuthTries 3
MaxSessions 2
ClientAliveInterval 300
ClientAliveCountMax 2
EOF

echo -e "${GREEN}[5/12] Configuring fail2ban for intrusion prevention...${NC}"
cat > /etc/fail2ban/jail.local <<'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
destemail = admin@sagatoy.com
sendername = Fail2Ban
action = %(action_mwl)s

[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 7200

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
filter = nginx-noscript
logpath = /var/log/nginx/access.log
maxretry = 6

[nginx-badbots]
enabled = true
port = http,https
filter = nginx-badbots
logpath = /var/log/nginx/access.log
maxretry = 2

[nginx-noproxy]
enabled = true
port = http,https
filter = nginx-noproxy
logpath = /var/log/nginx/access.log
maxretry = 2
EOF

systemctl enable fail2ban
systemctl restart fail2ban

echo -e "${GREEN}[6/12] Configuring strict firewall (UFW)...${NC}"
# Reset UFW to default deny
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# Allow only necessary ports
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Enable rate limiting on SSH
ufw limit 22/tcp

# Enable firewall
ufw --force enable
ufw status verbose

echo -e "${GREEN}[7/12] Stopping Apache if present...${NC}"
systemctl stop apache2 2>/dev/null || true
systemctl disable apache2 2>/dev/null || true

echo -e "${GREEN}[8/12] Creating website directory...${NC}"
mkdir -p /var/www/sagatoy.com
chown -R www-data:www-data /var/www/sagatoy.com
chmod -R 755 /var/www/sagatoy.com

echo -e "${GREEN}[9/12] Creating website homepage...${NC}"
cat > /var/www/sagatoy.com/index.html <<'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SagaToy - Secure & Online</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            text-align: center;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        h1 {
            font-size: 3.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .emoji { font-size: 4em; margin: 20px 0; }
        .status {
            font-size: 1.3em;
            color: #4ade80;
            font-weight: bold;
            margin: 20px 0;
        }
        .secure-badge {
            display: inline-block;
            background: #10b981;
            padding: 10px 20px;
            border-radius: 50px;
            margin: 10px;
            font-weight: bold;
        }
        .info {
            margin-top: 30px;
            font-size: 0.9em;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🎮</div>
        <h1>Welcome to SagaToy</h1>
        <p class="status">✓ Secure & Online</p>
        <div>
            <span class="secure-badge">🔒 SSL/TLS Encrypted</span>
            <span class="secure-badge">🛡️ Protected</span>
            <span class="secure-badge">⚡ Fast</span>
        </div>
        <div class="info">
            <p>Powered by Nginx + Let's Encrypt + Cloudflare</p>
            <p>Secured with fail2ban + UFW firewall</p>
        </div>
    </div>
</body>
</html>
EOF

echo -e "${GREEN}[10/12] Configuring Nginx with security headers...${NC}"
cat > /etc/nginx/sites-available/sagatoy.com <<'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name sagatoy.com www.sagatoy.com;

    root /var/www/sagatoy.com;
    index index.html index.htm;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Hide Nginx version
    server_tokens off;

    location / {
        try_files $uri $uri/ =404;
    }

    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Hide Nginx version globally
sed -i 's/# server_tokens off;/server_tokens off;/g' /etc/nginx/nginx.conf

# Test Nginx config
nginx -t

# Restart Nginx
systemctl restart nginx
systemctl enable nginx

echo -e "${YELLOW}[11/12] Obtaining SSL certificate...${NC}"
echo -e "${YELLOW}Make sure DNS is pointing to this server!${NC}"
read -p "Press Enter to continue with SSL setup, or Ctrl+C to abort..."

certbot --nginx \
    -d sagatoy.com \
    -d www.sagatoy.com \
    --non-interactive \
    --agree-tos \
    --email admin@sagatoy.com \
    --redirect

echo -e "${GREEN}[12/12] Setting up automatic SSL renewal...${NC}"
systemctl enable certbot.timer
systemctl start certbot.timer

# Test renewal
certbot renew --dry-run

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  SETUP COMPLETE!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "✅ SSL Certificate installed"
echo "✅ Nginx configured with security headers"
echo "✅ Firewall (UFW) enabled with strict rules"
echo "✅ Fail2ban configured for intrusion prevention"
echo "✅ SSH hardened (root login disabled, limited retries)"
echo "✅ Automatic security updates enabled"
echo "✅ SSL auto-renewal configured"
echo ""
echo -e "${YELLOW}Your website is now live at:${NC}"
echo "  🌐 https://sagatoy.com"
echo "  🌐 https://www.sagatoy.com"
echo ""
echo -e "${RED}IMPORTANT SECURITY TASKS:${NC}"
echo "1. Change your password NOW: passwd"
echo "2. Create a new non-root user:"
echo "   adduser yourusername"
echo "   usermod -aG sudo yourusername"
echo "3. Set up SSH key authentication"
echo "4. Consider changing SSH port from 22 to custom port"
echo ""
echo -e "${YELLOW}Security Services Status:${NC}"
fail2ban-client status
echo ""
ufw status
echo ""
echo -e "${GREEN}Setup completed successfully!${NC}"
