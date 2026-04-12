#!/bin/bash

################################################################################
# VPS Security Hardening Script with 2FA
#
# This script will secure your VPS with military-grade protection:
# - UFW Firewall with strict rules
# - SSH hardening (key + 2FA required)
# - Fail2Ban intrusion prevention
# - Automatic security updates
# - Nginx security headers
# - SSL/TLS ready configuration
#
# IMPORTANT SAFETY NOTES:
# 1. CREATE A VPS SNAPSHOT/BACKUP BEFORE RUNNING THIS!
# 2. Verify you have console access via your VPS provider's dashboard
# 3. Keep this SSH session open while testing
# 4. Test in a NEW terminal before closing this one
#
# Usage:
#   sudo bash secure_vps.sh
#
################################################################################

set -e  # Exit on error
trap 'echo "Error on line $LINENO. Exiting."; exit 1' ERR

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Function to print colored messages
print_header() {
    echo ""
    echo -e "${CYAN}${BOLD}========================================${NC}"
    echo -e "${CYAN}${BOLD}$1${NC}"
    echo -e "${CYAN}${BOLD}========================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Function to ask for confirmation
confirm() {
    while true; do
        read -p "$(echo -e ${YELLOW}$1 [y/n]: ${NC})" yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer yes (y) or no (n).";;
        esac
    done
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "This script must be run as root. Use: sudo bash $0"
    exit 1
fi

clear
print_header "VPS Security Hardening Script"

echo -e "${BOLD}This script will secure your VPS with:${NC}"
echo "  • UFW Firewall with strict rules"
echo "  • SSH hardening (disabled root, strong ciphers)"
echo "  • Two-Factor Authentication (2FA) setup"
echo "  • Fail2Ban intrusion prevention"
echo "  • Automatic security updates"
echo "  • Nginx security configurations"
echo ""
print_warning "BEFORE CONTINUING, ENSURE YOU HAVE:"
echo "  1. Created a VPS snapshot/backup"
echo "  2. Console access via your VPS provider's dashboard"
echo "  3. Google Authenticator app installed on your phone"
echo "  4. Keep this SSH session open during the entire process"
echo ""

if ! confirm "Have you completed all the above requirements?"; then
    print_error "Please complete the requirements before running this script."
    exit 1
fi

# Get current SSH port
CURRENT_SSH_PORT=$(grep "^Port " /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}')
if [ -z "$CURRENT_SSH_PORT" ]; then
    CURRENT_SSH_PORT=22
fi

# Ask about SSH port
echo ""
print_info "Current SSH port: $CURRENT_SSH_PORT"
if confirm "Do you want to change the SSH port? (Recommended for security)"; then
    while true; do
        read -p "Enter new SSH port (1024-65535): " NEW_SSH_PORT
        if [[ "$NEW_SSH_PORT" =~ ^[0-9]+$ ]] && [ "$NEW_SSH_PORT" -ge 1024 ] && [ "$NEW_SSH_PORT" -le 65535 ]; then
            CURRENT_SSH_PORT=$NEW_SSH_PORT
            print_success "SSH port will be changed to: $CURRENT_SSH_PORT"
            break
        else
            print_error "Invalid port. Must be between 1024 and 65535."
        fi
    done
fi

# Ask for username
echo ""
print_info "You should NOT use root for SSH access."
while true; do
    read -p "Enter the username you'll use for SSH (or create new): " SSH_USERNAME
    if [ ! -z "$SSH_USERNAME" ] && [ "$SSH_USERNAME" != "root" ]; then
        break
    else
        print_error "Username cannot be empty or 'root'. Please try again."
    fi
done

# Check if user exists
if id "$SSH_USERNAME" &>/dev/null; then
    print_info "User '$SSH_USERNAME' already exists."
    USER_EXISTS=true
else
    print_info "User '$SSH_USERNAME' will be created."
    USER_EXISTS=false
fi

# Create backup directory
BACKUP_DIR="/root/security_backups_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
print_info "Backup directory created: $BACKUP_DIR"

# Backup existing configurations
print_info "Backing up existing configurations..."
[ -f /etc/ssh/sshd_config ] && cp /etc/ssh/sshd_config "$BACKUP_DIR/sshd_config.bak"
[ -f /etc/fail2ban/jail.local ] && cp /etc/fail2ban/jail.local "$BACKUP_DIR/jail.local.bak"
[ -f /etc/ufw/user.rules ] && cp /etc/ufw/user.rules "$BACKUP_DIR/ufw_user.rules.bak"
print_success "Configurations backed up"

################################################################################
# PHASE 1: USER SETUP
################################################################################

print_header "Phase 1: User Setup"

if [ "$USER_EXISTS" = false ]; then
    print_info "Creating user: $SSH_USERNAME"
    adduser --gecos "" "$SSH_USERNAME"
    usermod -aG sudo "$SSH_USERNAME"
    print_success "User '$SSH_USERNAME' created and added to sudo group"
else
    print_info "Ensuring '$SSH_USERNAME' has sudo access..."
    usermod -aG sudo "$SSH_USERNAME"
    print_success "User '$SSH_USERNAME' has sudo access"
fi

# Set up SSH keys for user
print_info "Setting up SSH keys for $SSH_USERNAME..."
if [ -d "/root/.ssh" ] && [ -f "/root/.ssh/authorized_keys" ]; then
    mkdir -p "/home/$SSH_USERNAME/.ssh"
    cp /root/.ssh/authorized_keys "/home/$SSH_USERNAME/.ssh/"
    chown -R "$SSH_USERNAME:$SSH_USERNAME" "/home/$SSH_USERNAME/.ssh"
    chmod 700 "/home/$SSH_USERNAME/.ssh"
    chmod 600 "/home/$SSH_USERNAME/.ssh/authorized_keys"
    print_success "SSH keys copied to $SSH_USERNAME"
elif [ -d "/home/$SSH_USERNAME/.ssh" ] && [ -f "/home/$SSH_USERNAME/.ssh/authorized_keys" ]; then
    print_success "SSH keys already exist for $SSH_USERNAME"
else
    print_warning "No SSH keys found. You'll need to add your public key to /home/$SSH_USERNAME/.ssh/authorized_keys"
fi

################################################################################
# PHASE 2: FIREWALL CONFIGURATION
################################################################################

print_header "Phase 2: Firewall (UFW) Configuration"

print_info "Resetting UFW to default state..."
ufw --force reset >/dev/null

print_info "Setting default policies..."
ufw default deny incoming
ufw default allow outgoing

print_info "Allowing SSH on port $CURRENT_SSH_PORT..."
ufw allow $CURRENT_SSH_PORT/tcp comment 'SSH'

print_info "Allowing HTTP and HTTPS..."
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Ask about additional ports
echo ""
if confirm "Do you need to open any additional ports?"; then
    while true; do
        read -p "Enter port number (or press Enter to finish): " EXTRA_PORT
        if [ -z "$EXTRA_PORT" ]; then
            break
        fi
        if [[ "$EXTRA_PORT" =~ ^[0-9]+$ ]]; then
            read -p "Protocol (tcp/udp): " PROTOCOL
            read -p "Description: " DESCRIPTION
            ufw allow $EXTRA_PORT/$PROTOCOL comment "$DESCRIPTION"
            print_success "Port $EXTRA_PORT/$PROTOCOL added"
        else
            print_error "Invalid port number"
        fi
    done
fi

print_info "Enabling UFW firewall..."
echo "y" | ufw enable >/dev/null

print_success "Firewall configured and enabled"
echo ""
ufw status verbose

################################################################################
# PHASE 3: SSH HARDENING
################################################################################

print_header "Phase 3: SSH Hardening"

# Change SSH port if requested
if [ "$CURRENT_SSH_PORT" != "22" ]; then
    print_info "Changing SSH port to $CURRENT_SSH_PORT..."
    if grep -q "^Port " /etc/ssh/sshd_config; then
        sed -i "s/^Port .*/Port $CURRENT_SSH_PORT/" /etc/ssh/sshd_config
    else
        echo "Port $CURRENT_SSH_PORT" >> /etc/ssh/sshd_config
    fi
    print_success "SSH port changed to $CURRENT_SSH_PORT"
fi

print_info "Creating SSH hardening configuration..."
cat > /etc/ssh/sshd_config.d/99-hardening.conf << 'EOF'
# SSH Security Hardening Configuration

# Disable root login
PermitRootLogin no

# Use only public key authentication (password auth disabled after 2FA setup)
# Uncomment the next line AFTER 2FA is working:
# PasswordAuthentication no
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

# Keep connection alive
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

# Limit sessions and connections
MaxSessions 2
MaxStartups 10:30:60

# Verbose logging
LogLevel VERBOSE
EOF

print_success "SSH hardening configuration created"

print_info "Testing SSH configuration..."
if sshd -t; then
    print_success "SSH configuration is valid"
else
    print_error "SSH configuration has errors! Check the output above."
    exit 1
fi

################################################################################
# PHASE 4: FAIL2BAN CONFIGURATION
################################################################################

print_header "Phase 4: Fail2Ban Configuration"

print_info "Configuring Fail2Ban..."
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
# Ban time: 1 hour
bantime = 3600

# A host is banned if it generates "maxretry" during the last "findtime"
findtime = 600
maxretry = 3

# Email configuration
destemail = root@localhost
sender = fail2ban@localhost
action = %(action_mwl)s

# Ignore local connections
ignoreip = 127.0.0.1/8 ::1

# SSH jail
[sshd]
enabled = true
port = $CURRENT_SSH_PORT
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

# Nginx jails
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

print_info "Restarting Fail2Ban..."
systemctl restart fail2ban
systemctl enable fail2ban >/dev/null 2>&1

print_success "Fail2Ban configured and running"
echo ""
fail2ban-client status

################################################################################
# PHASE 5: AUTOMATIC SECURITY UPDATES
################################################################################

print_header "Phase 5: Automatic Security Updates"

print_info "Configuring automatic security updates..."
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

print_success "Automatic security updates configured"

################################################################################
# PHASE 6: NGINX SECURITY
################################################################################

print_header "Phase 6: Nginx Security Configuration"

if systemctl is-active --quiet nginx; then
    print_info "Nginx is installed. Creating security configurations..."

    # Security headers
    cat > /etc/nginx/snippets/security-headers.conf << 'EOF'
# Security Headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

# Remove server version
server_tokens off;
EOF

    # SSL configuration
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

# Uncomment after generating dhparam:
# ssl_dhparam /etc/nginx/dhparam.pem;
EOF

    print_success "Nginx security configurations created"
    print_info "To use in your server blocks, add:"
    echo "    include snippets/security-headers.conf;"
    echo "    include snippets/ssl-params.conf;"
else
    print_warning "Nginx not detected. Skipping Nginx configuration."
fi

################################################################################
# PHASE 7: 2FA SETUP INSTRUCTIONS
################################################################################

print_header "Phase 7: Two-Factor Authentication (2FA) Setup"

print_warning "2FA setup requires interactive configuration."
echo ""
echo -e "${BOLD}You need to complete these steps:${NC}"
echo ""
echo "1. Switch to your user account:"
echo -e "   ${CYAN}su - $SSH_USERNAME${NC}"
echo ""
echo "2. Run Google Authenticator setup:"
echo -e "   ${CYAN}google-authenticator${NC}"
echo ""
echo "3. Answer the prompts:"
echo "   - Time-based tokens? ${GREEN}y${NC}"
echo "   - ${YELLOW}SCAN QR CODE WITH YOUR PHONE${NC}"
echo "   - ${RED}SAVE THE EMERGENCY CODES!${NC} (Very important!)"
echo "   - Update .google_authenticator file? ${GREEN}y${NC}"
echo "   - Disallow token reuse? ${GREEN}y${NC}"
echo "   - Increase time window? ${GREEN}n${NC}"
echo "   - Enable rate-limiting? ${GREEN}y${NC}"
echo ""
echo "4. Configure PAM (as root):"
echo -e "   ${CYAN}sudo nano /etc/pam.d/sshd${NC}"
echo "   Add at the TOP:"
echo -e "   ${GREEN}auth required pam_google_authenticator.so nullok${NC}"
echo "   Comment out:"
echo -e "   ${YELLOW}# @include common-auth${NC}"
echo ""
echo "5. Configure SSH for 2FA (as root):"
echo -e "   ${CYAN}sudo nano /etc/ssh/sshd_config${NC}"
echo "   Add these lines:"
echo -e "   ${GREEN}ChallengeResponseAuthentication yes${NC}"
echo -e "   ${GREEN}UsePAM yes${NC}"
echo -e "   ${GREEN}AuthenticationMethods publickey,keyboard-interactive${NC}"
echo ""
echo "6. Test SSH configuration:"
echo -e "   ${CYAN}sudo sshd -t${NC}"
echo ""
echo "7. Restart SSH:"
echo -e "   ${CYAN}sudo systemctl restart sshd${NC}"
echo ""
echo "8. ${RED}IMPORTANT:${NC} Test login in a NEW terminal BEFORE closing this one:"
echo -e "   ${CYAN}ssh $SSH_USERNAME@<your-vps-ip> -p $CURRENT_SSH_PORT${NC}"
echo ""
echo "9. After 2FA works, disable password authentication:"
echo -e "   ${CYAN}sudo nano /etc/ssh/sshd_config.d/99-hardening.conf${NC}"
echo "   Uncomment:"
echo -e "   ${GREEN}PasswordAuthentication no${NC}"
echo "   Then:"
echo -e "   ${CYAN}sudo systemctl restart sshd${NC}"
echo ""

# Create a helper script for 2FA setup
cat > /root/setup_2fa_step2.sh << 'EOFSCRIPT'
#!/bin/bash

# 2FA Setup - Step 2
# Run this script to complete 2FA configuration

echo "Configuring PAM for 2FA..."
if ! grep -q "pam_google_authenticator.so" /etc/pam.d/sshd; then
    sed -i '1s/^/auth required pam_google_authenticator.so nullok\n/' /etc/pam.d/sshd
    sed -i 's/^@include common-auth/#@include common-auth/' /etc/pam.d/sshd
    echo "✓ PAM configured"
else
    echo "✓ PAM already configured"
fi

echo "Configuring SSH for 2FA..."
if ! grep -q "AuthenticationMethods publickey,keyboard-interactive" /etc/ssh/sshd_config; then
    cat >> /etc/ssh/sshd_config << EOF

# 2FA Configuration
ChallengeResponseAuthentication yes
UsePAM yes
AuthenticationMethods publickey,keyboard-interactive
EOF
    echo "✓ SSH configured for 2FA"
else
    echo "✓ SSH already configured for 2FA"
fi

echo "Testing SSH configuration..."
if sshd -t; then
    echo "✓ SSH configuration is valid"
    echo ""
    echo "Restarting SSH service..."
    systemctl restart sshd
    echo "✓ SSH service restarted"
    echo ""
    echo "2FA is now active!"
    echo ""
    echo "⚠ TEST LOGIN IN A NEW TERMINAL BEFORE CLOSING THIS ONE!"
    echo ""
else
    echo "✗ SSH configuration has errors!"
    exit 1
fi
EOFSCRIPT

chmod +x /root/setup_2fa_step2.sh

print_success "Created helper script: /root/setup_2fa_step2.sh"
print_info "After running google-authenticator, run: sudo /root/setup_2fa_step2.sh"

################################################################################
# PHASE 8: FINAL STEPS
################################################################################

print_header "Phase 8: Final Configuration"

print_info "Setting secure file permissions..."
chmod 600 /etc/ssh/sshd_config
chmod 700 /home/$SSH_USERNAME/.ssh 2>/dev/null || true
chmod 600 /home/$SSH_USERNAME/.ssh/authorized_keys 2>/dev/null || true
print_success "File permissions secured"

print_info "Restarting SSH service..."
systemctl restart sshd
print_success "SSH service restarted"

################################################################################
# COMPLETION
################################################################################

print_header "Security Hardening Complete!"

echo -e "${GREEN}${BOLD}✓ Base security configuration completed!${NC}"
echo ""
echo -e "${BOLD}What was configured:${NC}"
echo "  ✓ UFW Firewall (SSH port $CURRENT_SSH_PORT, HTTP, HTTPS)"
echo "  ✓ SSH hardening (root login disabled, strong ciphers)"
echo "  ✓ Fail2Ban intrusion prevention"
echo "  ✓ Automatic security updates"
echo "  ✓ Nginx security headers (if applicable)"
echo "  ✓ User '$SSH_USERNAME' ready for SSH access"
echo ""
echo -e "${YELLOW}${BOLD}CRITICAL NEXT STEPS:${NC}"
echo ""
echo "1. ${BOLD}Set up 2FA NOW:${NC}"
echo -e "   ${CYAN}su - $SSH_USERNAME${NC}"
echo -e "   ${CYAN}google-authenticator${NC}"
echo "   Then run: ${CYAN}sudo /root/setup_2fa_step2.sh${NC}"
echo ""
echo "2. ${BOLD}Test SSH in a NEW terminal:${NC}"
echo -e "   ${CYAN}ssh $SSH_USERNAME@<your-vps-ip> -p $CURRENT_SSH_PORT${NC}"
echo "   ${RED}DO NOT CLOSE THIS SESSION until new login works!${NC}"
echo ""
echo "3. ${BOLD}After 2FA works, disable password auth:${NC}"
echo -e "   Edit: ${CYAN}/etc/ssh/sshd_config.d/99-hardening.conf${NC}"
echo -e "   Uncomment: ${GREEN}PasswordAuthentication no${NC}"
echo -e "   Restart: ${CYAN}sudo systemctl restart sshd${NC}"
echo ""
echo -e "${BOLD}Optional enhancements:${NC}"
echo "  • Generate DH params for Nginx:"
echo -e "    ${CYAN}sudo openssl dhparam -out /etc/nginx/dhparam.pem 4096${NC}"
echo ""
echo "  • Set up SSL with Certbot:"
echo -e "    ${CYAN}sudo certbot --nginx -d yourdomain.com${NC}"
echo ""
echo -e "${BOLD}Backup location:${NC} $BACKUP_DIR"
echo ""
echo -e "${BOLD}Emergency access:${NC} Use your VPS provider's web console"
echo ""
echo -e "${GREEN}${BOLD}Your VPS is now significantly more secure! 🛡️${NC}"
echo ""
print_warning "Remember: SAVE YOUR 2FA EMERGENCY CODES in a password manager!"
echo ""
