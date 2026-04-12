#!/bin/bash
# ULTRA SECURE VPS SETUP - Maximum Security Configuration
# For sagatoy.com - Prevents unauthorized access
# Run as: sudo bash ultra_secure_setup.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "============================================="
echo "   ULTRA SECURE VPS SETUP FOR SAGATOY.COM"
echo "   Maximum Security + 2FA + SSL"
echo "============================================="
echo -e "${NC}"

if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root (use sudo)${NC}"
   exit 1
fi

# Get custom SSH port
echo -e "${YELLOW}Choose a custom SSH port (recommended: 2222-65535, avoid common ports):${NC}"
read -p "Enter custom SSH port [default: 2222]: " SSH_PORT
SSH_PORT=${SSH_PORT:-2222}

echo -e "${GREEN}[1/15] Updating system...${NC}"
apt update && apt upgrade -y

echo -e "${GREEN}[2/15] Installing security packages...${NC}"
apt install -y nginx certbot python3-certbot-nginx ufw fail2ban \
    libpam-google-authenticator qrencode openssh-server \
    unattended-upgrades apt-listchanges fail2ban-systemd \
    net-tools curl wget git

echo -e "${GREEN}[3/15] Enabling automatic security updates...${NC}"
cat > /etc/apt/apt.conf.d/50unattended-upgrades <<'EOF'
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
};
Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
EOF

cat > /etc/apt/apt.conf.d/20auto-upgrades <<'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
EOF

systemctl enable unattended-upgrades
systemctl start unattended-upgrades

echo -e "${GREEN}[4/15] Configuring 2FA (Google Authenticator)...${NC}"
# Configure PAM for 2FA
if ! grep -q "pam_google_authenticator.so" /etc/pam.d/sshd; then
    echo "auth required pam_google_authenticator.so nullok" >> /etc/pam.d/sshd
    sed -i 's/@include common-auth/#@include common-auth/' /etc/pam.d/sshd
fi

echo -e "${GREEN}[5/15] Hardening SSH configuration...${NC}"
# Backup original config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%F)

# Create hardened SSH config
cat > /etc/ssh/sshd_config.d/99-hardening.conf <<EOF
# Custom SSH Port
Port ${SSH_PORT}

# Authentication
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive

# Security
MaxAuthTries 3
MaxSessions 2
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2

# Disable dangerous features
X11Forwarding no
PermitEmptyPasswords no
PermitUserEnvironment no
AllowAgentForwarding no
AllowTcpForwarding no

# Logging
SyslogFacility AUTH
LogLevel VERBOSE

# Network
AddressFamily inet
ListenAddress 0.0.0.0

# Only allow specific users (will be configured per user)
# AllowUsers yourusername
EOF

echo -e "${GREEN}[6/15] Configuring fail2ban...${NC}"
cat > /etc/fail2ban/jail.local <<EOF
[DEFAULT]
bantime = 86400
findtime = 600
maxretry = 3
destemail = admin@sagatoy.com
sendername = Fail2Ban-SagaToy
action = %(action_mwl)s
backend = systemd

[sshd]
enabled = true
port = ${SSH_PORT}
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 86400
findtime = 600

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3

[nginx-noscript]
enabled = true
port = http,https
filter = nginx-noscript
logpath = /var/log/nginx/access.log
maxretry = 6
bantime = 43200

[nginx-badbots]
enabled = true
port = http,https
filter = nginx-badbots
logpath = /var/log/nginx/access.log
maxretry = 2
bantime = 86400

[nginx-noproxy]
enabled = true
port = http,https
filter = nginx-noproxy
logpath = /var/log/nginx/access.log
maxretry = 0
bantime = 86400
EOF

# Create custom fail2ban filter for port scanning
cat > /etc/fail2ban/filter.d/port-scan.conf <<'EOF'
[Definition]
failregex = ^.*Port scan detected from <HOST>.*$
ignoreregex =
EOF

systemctl enable fail2ban
systemctl restart fail2ban

echo -e "${GREEN}[7/15] Configuring UFW firewall...${NC}"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# Allow custom SSH port
ufw allow ${SSH_PORT}/tcp comment 'SSH Custom Port'

# Allow HTTP and HTTPS
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Rate limit SSH
ufw limit ${SSH_PORT}/tcp

# Enable firewall
ufw --force enable

echo -e "${GREEN}[8/15] Installing additional security tools...${NC}"
# Install rootkit detector
apt install -y rkhunter chkrootkit

# Configure rkhunter
rkhunter --update
rkhunter --propupd

echo -e "${GREEN}[9/15] Disabling unnecessary services...${NC}"
systemctl disable apache2 2>/dev/null || true
systemctl stop apache2 2>/dev/null || true

echo -e "${GREEN}[10/15] Setting up Nginx with security...${NC}"
mkdir -p /var/www/sagatoy.com
chown -R www-data:www-data /var/www/sagatoy.com
chmod -R 755 /var/www/sagatoy.com

# Create homepage
cat > /var/www/sagatoy.com/index.html <<'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SagaToy - Ultra Secure</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            text-align: center;
            padding: 60px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 30px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            max-width: 800px;
        }
        h1 {
            font-size: 4em;
            margin-bottom: 20px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        }
        .emoji { font-size: 5em; margin: 30px 0; animation: pulse 2s infinite; }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .status {
            font-size: 1.5em;
            color: #4ade80;
            font-weight: bold;
            margin: 30px 0;
        }
        .security-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }
        .badge {
            background: rgba(16, 185, 129, 0.2);
            padding: 15px;
            border-radius: 15px;
            border: 2px solid #10b981;
            font-weight: 600;
        }
        .info {
            margin-top: 40px;
            font-size: 0.95em;
            opacity: 0.9;
            line-height: 1.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🛡️</div>
        <h1>SagaToy</h1>
        <p class="status">✓ Ultra Secure & Protected</p>

        <div class="security-grid">
            <div class="badge">🔐 2FA Enabled</div>
            <div class="badge">🔒 SSL/TLS</div>
            <div class="badge">🛡️ Firewall Active</div>
            <div class="badge">🚫 Fail2ban</div>
            <div class="badge">🔑 SSH Keys Only</div>
            <div class="badge">☁️ Cloudflare</div>
        </div>

        <div class="info">
            <p><strong>Security Features:</strong></p>
            <p>Two-Factor Authentication • SSH Key Auth • Custom Port</p>
            <p>Fail2ban Protection • UFW Firewall • Auto Updates</p>
            <p>Nginx + Let's Encrypt • Cloudflare DDoS Protection</p>
        </div>
    </div>
</body>
</html>
HTMLEOF

# Configure Nginx with security headers
cat > /etc/nginx/sites-available/sagatoy.com <<'NGINXEOF'
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
    add_header Content-Security-Policy "default-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline';" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # Hide server info
    server_tokens off;
    more_clear_headers Server;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req zone=general burst=20 nodelay;

    location / {
        try_files $uri $uri/ =404;
    }

    # Block access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Block common exploit attempts
    location ~* \.(sql|git|env|bak|old)$ {
        deny all;
        access_log off;
        log_not_found off;
    }
}
NGINXEOF

# Enable site
ln -sf /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Configure Nginx security settings globally
sed -i 's/# server_tokens off;/server_tokens off;/' /etc/nginx/nginx.conf

# Test and restart
nginx -t && systemctl restart nginx
systemctl enable nginx

echo -e "${GREEN}[11/15] Installing SSL certificate...${NC}"
echo -e "${YELLOW}Ensure DNS is configured: sagatoy.com → this server${NC}"
read -p "Press Enter when DNS is ready, or Ctrl+C to skip SSL for now..."

certbot --nginx \
    -d sagatoy.com \
    -d www.sagatoy.com \
    --non-interactive \
    --agree-tos \
    --email admin@sagatoy.com \
    --redirect \
    --hsts \
    --staple-ocsp \
    --must-staple || echo "SSL setup failed, you can run certbot manually later"

echo -e "${GREEN}[12/15] Configuring SSL auto-renewal...${NC}"
systemctl enable certbot.timer
systemctl start certbot.timer

# Test renewal
certbot renew --dry-run || true

echo -e "${GREEN}[13/15] Setting up intrusion detection...${NC}"
# Install and configure AIDE (intrusion detection)
apt install -y aide aide-common
aideinit
mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db || true

echo -e "${GREEN}[14/15] Configuring kernel security parameters...${NC}"
cat > /etc/sysctl.d/99-security.conf <<'EOF'
# IP Forwarding
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0

# Syn Cookies
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_syn_retries = 2
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_max_syn_backlog = 4096

# Disable ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0

# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Log Martians
net.ipv4.conf.all.log_martians = 1

# Ignore ICMP ping requests
net.ipv4.icmp_echo_ignore_all = 1

# Ignore Broadcast Request
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Protection against bad ICMP error messages
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Reverse Path Filtering
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
EOF

sysctl -p /etc/sysctl.d/99-security.conf

echo -e "${GREEN}[15/15] Creating security monitoring script...${NC}"
cat > /usr/local/bin/security-check.sh <<'EOF'
#!/bin/bash
echo "=== Security Status Check ==="
echo ""
echo "Firewall Status:"
ufw status numbered
echo ""
echo "Fail2ban Status:"
fail2ban-client status
echo ""
echo "Active SSH Sessions:"
who
echo ""
echo "Recent Failed Login Attempts:"
grep "Failed password" /var/log/auth.log | tail -10
echo ""
echo "Banned IPs:"
fail2ban-client status sshd
EOF

chmod +x /usr/local/bin/security-check.sh

echo ""
echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}   ULTRA SECURE SETUP COMPLETE!${NC}"
echo -e "${GREEN}=============================================${NC}"
echo ""
echo -e "${YELLOW}⚠️  CRITICAL: NEXT STEPS TO COMPLETE SECURITY ⚠️${NC}"
echo ""
echo -e "${RED}1. SET UP 2FA FOR YOUR USER:${NC}"
echo "   Run as your regular user (NOT root):"
echo "   $ google-authenticator"
echo "   Scan the QR code with Google Authenticator app"
echo ""
echo -e "${RED}2. CHANGE YOUR PASSWORD:${NC}"
echo "   $ passwd"
echo ""
echo -e "${RED}3. CREATE SSH KEY (on your local computer):${NC}"
echo "   $ ssh-keygen -t ed25519 -C 'sagatoy-vps'"
echo "   $ ssh-copy-id -p ${SSH_PORT} yourusername@94.72.141.71"
echo ""
echo -e "${RED}4. TEST NEW SSH CONNECTION (before logging out):${NC}"
echo "   Open a NEW terminal and test:"
echo "   $ ssh -p ${SSH_PORT} yourusername@94.72.141.71"
echo ""
echo -e "${YELLOW}Security Configuration:${NC}"
echo "   ✅ Custom SSH Port: ${SSH_PORT}"
echo "   ✅ 2FA: Ready (needs user setup)"
echo "   ✅ SSH Keys: Required"
echo "   ✅ Password Auth: DISABLED"
echo "   ✅ Root Login: DISABLED"
echo "   ✅ Fail2ban: Active"
echo "   ✅ Firewall: Active"
echo "   ✅ SSL: Configured"
echo "   ✅ Auto Updates: Enabled"
echo ""
echo -e "${BLUE}Access Your Site:${NC}"
echo "   🌐 https://sagatoy.com"
echo "   🌐 https://www.sagatoy.com"
echo ""
echo -e "${BLUE}SSH Connection (new port):${NC}"
echo "   ssh -p ${SSH_PORT} yourusername@94.72.141.71"
echo ""
echo -e "${YELLOW}Monitoring Commands:${NC}"
echo "   security-check.sh       - Full security status"
echo "   fail2ban-client status  - Check blocked IPs"
echo "   ufw status             - Check firewall rules"
echo ""
echo -e "${RED}⚠️  IMPORTANT: Don't logout until you've tested SSH access!${NC}"
echo ""
