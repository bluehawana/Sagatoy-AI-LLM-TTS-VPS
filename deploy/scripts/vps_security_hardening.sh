#!/bin/bash
# VPS Security Hardening Script
# Run this on your VPS via SSH
# WARNING: Review this script before running. Improper firewall rules can lock you out!

set -e  # Exit on any error

echo "=================================="
echo "VPS Security Hardening Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# Get current SSH port
CURRENT_SSH_PORT=$(grep "^Port " /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}')
if [ -z "$CURRENT_SSH_PORT" ]; then
    CURRENT_SSH_PORT=22
fi

echo -e "${YELLOW}Current SSH port: $CURRENT_SSH_PORT${NC}"
echo ""

# Backup existing configurations
echo "Creating backups of existing configurations..."
mkdir -p /root/security_backups_$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/root/security_backups_$(date +%Y%m%d_%H%M%S)"
cp /etc/ssh/sshd_config "$BACKUP_DIR/sshd_config.bak" 2>/dev/null || true
cp /etc/fail2ban/jail.local "$BACKUP_DIR/jail.local.bak" 2>/dev/null || true
echo -e "${GREEN}Backups saved to: $BACKUP_DIR${NC}"
echo ""

#############################################
# 1. CONFIGURE UFW FIREWALL
#############################################
echo "=== Configuring UFW Firewall ==="

# Reset UFW to default
ufw --force reset

# Set default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (current port)
echo "Allowing SSH on port $CURRENT_SSH_PORT..."
ufw allow $CURRENT_SSH_PORT/tcp comment 'SSH'

# Allow HTTP and HTTPS for Nginx
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Enable UFW
echo "y" | ufw enable

echo -e "${GREEN}UFW firewall configured and enabled${NC}"
ufw status verbose
echo ""

#############################################
# 2. HARDEN SSH CONFIGURATION
#############################################
echo "=== Hardening SSH Configuration ==="

# Create SSH hardening config
cat > /etc/ssh/sshd_config.d/99-hardening.conf << 'EOF'
# SSH Hardening Configuration

# Disable root login
PermitRootLogin no

# Use only SSH keys (disable password authentication after 2FA is set up)
# PasswordAuthentication no  # UNCOMMENT AFTER 2FA IS WORKING
PubkeyAuthentication yes

# Disable empty passwords
PermitEmptyPasswords no

# Disable X11 forwarding
X11Forwarding no

# Disable agent forwarding
AllowAgentForwarding no

# Disable TCP forwarding
AllowTcpForwarding no

# Set maximum authentication attempts
MaxAuthTries 3

# Set login grace time
LoginGraceTime 30

# Set client alive interval (keep connection alive)
ClientAliveInterval 300
ClientAliveCountMax 2

# Disable unused authentication methods
ChallengeResponseAuthentication no
KerberosAuthentication no
GSSAPIAuthentication no

# Use strong ciphers only
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group-exchange-sha256

# Set maximum sessions
MaxSessions 2

# Set maximum startups
MaxStartups 10:30:60

# Log verbosity
LogLevel VERBOSE
EOF

echo -e "${GREEN}SSH hardening configuration created${NC}"
echo -e "${YELLOW}Note: PasswordAuthentication will be disabled after 2FA is set up${NC}"
echo ""

# Test SSH configuration
echo "Testing SSH configuration..."
sshd -t
if [ $? -eq 0 ]; then
    echo -e "${GREEN}SSH configuration is valid${NC}"
else
    echo -e "${RED}SSH configuration has errors!${NC}"
    exit 1
fi
echo ""

#############################################
# 3. CONFIGURE FAIL2BAN
#############################################
echo "=== Configuring Fail2Ban ==="

# Create jail.local configuration
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
# Ban hosts for 1 hour
bantime = 3600

# A host is banned if it has generated "maxretry" during the last "findtime"
findtime = 600
maxretry = 3

# Destination email for ban notifications
destemail = root@localhost
sender = fail2ban@localhost

# Action: ban & send email
action = %(action_mwl)s

# Ignore local connections
ignoreip = 127.0.0.1/8 ::1

[sshd]
enabled = true
port = $CURRENT_SSH_PORT
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

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

# Restart fail2ban
systemctl restart fail2ban
systemctl enable fail2ban

echo -e "${GREEN}Fail2Ban configured and running${NC}"
fail2ban-client status
echo ""

#############################################
# 4. CONFIGURE AUTOMATIC SECURITY UPDATES
#############################################
echo "=== Configuring Automatic Security Updates ==="

# Configure unattended-upgrades
cat > /etc/apt/apt.conf.d/50unattended-upgrades << 'EOF'
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
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
EOF

cat > /etc/apt/apt.conf.d/20auto-upgrades << 'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
EOF

echo -e "${GREEN}Automatic security updates configured${NC}"
echo ""

#############################################
# 5. SECURE NGINX CONFIGURATION
#############################################
echo "=== Securing Nginx Configuration ==="

# Create security headers configuration
cat > /etc/nginx/snippets/security-headers.conf << 'EOF'
# Security Headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

# Remove version disclosure
server_tokens off;
EOF

# Create SSL configuration
cat > /etc/nginx/snippets/ssl-params.conf << 'EOF'
# SSL Configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
ssl_ecdh_curve secp384r1;
ssl_session_timeout 10m;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;

# Diffie-Hellman parameter for DHE ciphersuites
# Generate with: openssl dhparam -out /etc/nginx/dhparam.pem 4096
# ssl_dhparam /etc/nginx/dhparam.pem;
EOF

echo -e "${GREEN}Nginx security configurations created${NC}"
echo -e "${YELLOW}Include these in your server blocks:${NC}"
echo "  include snippets/security-headers.conf;"
echo "  include snippets/ssl-params.conf;"
echo ""

#############################################
# 6. ADDITIONAL SECURITY MEASURES
#############################################
echo "=== Additional Security Measures ==="

# Disable unnecessary services
echo "Checking for unnecessary services..."
systemctl disable --now apache2 2>/dev/null || true
echo -e "${GREEN}Unnecessary services checked${NC}"

# Set proper file permissions
echo "Setting secure file permissions..."
chmod 600 /etc/ssh/sshd_config
chmod 700 ~/.ssh 2>/dev/null || true
chmod 600 ~/.ssh/authorized_keys 2>/dev/null || true

echo -e "${GREEN}File permissions secured${NC}"
echo ""

#############################################
# RESTART SERVICES
#############################################
echo "=== Restarting Services ==="
systemctl restart sshd
systemctl restart nginx 2>/dev/null || echo "Nginx not fully configured yet"
systemctl restart fail2ban

echo ""
echo "=================================="
echo -e "${GREEN}Security Hardening Complete!${NC}"
echo "=================================="
echo ""
echo "NEXT STEPS:"
echo "1. Set up 2FA with Google Authenticator (see 2fa_setup_guide.md)"
echo "2. Generate Diffie-Hellman parameters: openssl dhparam -out /etc/nginx/dhparam.pem 4096"
echo "3. Set up SSL certificates: certbot --nginx -d yourdomain.com"
echo "4. Create a non-root user if you haven't already"
echo "5. Test SSH access in a NEW terminal before closing this one!"
echo ""
echo -e "${YELLOW}WARNING: Before disconnecting, test SSH in a new terminal!${NC}"
echo ""
