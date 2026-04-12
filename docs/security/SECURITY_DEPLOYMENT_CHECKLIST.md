# VPS Security Deployment Checklist

## Pre-Deployment Preparation

### ☐ 1. Backup Current State
```bash
# Create a snapshot/backup through your VPS provider's dashboard
# Most providers offer one-click snapshots
```

### ☐ 2. Document Current Settings
Write down:
- Current SSH port: __________
- Current username: __________
- Root login status: __________
- Your static IP (if any): __________
- VPS provider console URL: __________

### ☐ 3. Install Google Authenticator App
- [ ] iOS: Download from App Store
- [ ] Android: Download from Google Play Store

### ☐ 4. Prepare Secure Storage
- [ ] Password manager ready (for emergency codes)
- [ ] Secure place for emergency code backup (encrypted USB, printed copy in safe, etc.)

## Deployment Steps

### Phase 1: Initial Security Hardening (30-45 minutes)

#### ☐ Step 1: Upload Security Script to VPS
```bash
# On your local machine, upload the script
scp vps_security_hardening.sh your-username@your-vps-ip:/tmp/

# SSH into your VPS
ssh your-username@your-vps-ip

# Move script and make executable
sudo mv /tmp/vps_security_hardening.sh /root/
sudo chmod +x /root/vps_security_hardening.sh
```

#### ☐ Step 2: Review the Script
```bash
# IMPORTANT: Review the script before running
sudo less /root/vps_security_hardening.sh

# Check what ports will be opened
# Verify SSH port matches your current configuration
```

#### ☐ Step 3: Run Security Hardening Script
```bash
# Run the script
sudo /root/vps_security_hardening.sh

# Expected duration: 2-5 minutes
```

#### ☐ Step 4: Verify Services Started
```bash
# Check UFW
sudo ufw status verbose

# Check Fail2Ban
sudo systemctl status fail2ban

# Check SSH
sudo systemctl status sshd

# Check Nginx
sudo systemctl status nginx
```

**CHECKPOINT: Do NOT proceed if any service failed to start**

### Phase 2: User Setup (10-15 minutes)

#### ☐ Step 5: Create Non-Root User (if not exists)
```bash
# Create user (replace 'yourname' with your desired username)
sudo adduser yourname

# Add to sudo group
sudo usermod -aG sudo yourname

# Set a strong password when prompted
```

#### ☐ Step 6: Set Up SSH Keys for New User
```bash
# Create .ssh directory
sudo mkdir -p /home/yourname/.ssh

# Copy authorized keys from current user
sudo cp ~/.ssh/authorized_keys /home/yourname/.ssh/

# Set proper ownership
sudo chown -R yourname:yourname /home/yourname/.ssh
sudo chmod 700 /home/yourname/.ssh
sudo chmod 600 /home/yourname/.ssh/authorized_keys
```

#### ☐ Step 7: Test New User Access
**IMPORTANT: Open a NEW terminal window, keep current session open!**

```bash
# In NEW terminal:
ssh yourname@your-vps-ip

# Verify you can:
# 1. Log in with SSH key
# 2. Run sudo commands: sudo ls /root
```

**CHECKPOINT: Do NOT proceed until new user login works**

### Phase 3: Two-Factor Authentication Setup (15-20 minutes)

#### ☐ Step 8: Run Google Authenticator Setup
```bash
# Log in as your non-root user
ssh yourname@your-vps-ip

# Run Google Authenticator
google-authenticator
```

#### ☐ Step 9: Answer Setup Questions
Follow the prompts (see detailed guide in `2fa_setup_guide.md`):
1. [ ] Time-based tokens: **y**
2. [ ] **SAVE EMERGENCY CODES** ← CRITICAL!
3. [ ] Scan QR code with your phone
4. [ ] Update .google_authenticator file: **y**
5. [ ] Disallow token reuse: **y**
6. [ ] Increase time window: **n**
7. [ ] Enable rate-limiting: **y**

#### ☐ Step 10: Save Emergency Codes IMMEDIATELY
**BEFORE CONTINUING:**
- [ ] Copy emergency scratch codes to password manager
- [ ] Save a second backup (printed copy, encrypted file, etc.)
- [ ] Verify you can access these codes from a different device

#### ☐ Step 11: Configure PAM for 2FA
```bash
sudo nano /etc/pam.d/sshd
```

Add at the TOP:
```
auth required pam_google_authenticator.so nullok
```

Comment out:
```
# @include common-auth
```

Save and exit (Ctrl+X, Y, Enter)

#### ☐ Step 12: Configure SSH for 2FA
```bash
sudo nano /etc/ssh/sshd_config
```

Add or modify:
```
ChallengeResponseAuthentication yes
UsePAM yes
AuthenticationMethods publickey,keyboard-interactive
```

Save and exit

#### ☐ Step 13: Test SSH Configuration
```bash
# Test for syntax errors
sudo sshd -t

# Should return nothing if successful
```

**CHECKPOINT: Fix any errors before proceeding**

#### ☐ Step 14: Restart SSH Service
```bash
sudo systemctl restart sshd
```

#### ☐ Step 15: Test 2FA Login
**CRITICAL: Keep your current SSH session open!**

**In a NEW terminal:**
```bash
ssh yourname@your-vps-ip

# You should be prompted for:
# 1. SSH key passphrase (if you have one)
# 2. Verification code from Google Authenticator
```

**Tests to perform:**
- [ ] Can log in with correct 2FA code
- [ ] Cannot log in with wrong 2FA code
- [ ] Can log in with emergency scratch code
- [ ] Old session still works

**CHECKPOINT: Do NOT close original session until this works!**

### Phase 4: Final Hardening (10 minutes)

#### ☐ Step 16: Disable Root Login
```bash
sudo nano /etc/ssh/sshd_config.d/99-hardening.conf
```

Verify this line exists and is not commented:
```
PermitRootLogin no
```

#### ☐ Step 17: Disable Password Authentication
Once 2FA is confirmed working:
```bash
sudo nano /etc/ssh/sshd_config.d/99-hardening.conf
```

Uncomment:
```
PasswordAuthentication no
```

#### ☐ Step 18: Restart SSH and Test Again
```bash
sudo systemctl restart sshd

# Test in NEW terminal
ssh yourname@your-vps-ip
```

#### ☐ Step 19: Remove 'nullok' from PAM
After confirming all users have 2FA:
```bash
sudo nano /etc/pam.d/sshd
```

Change:
```
auth required pam_google_authenticator.so
```
(Remove `nullok`)

#### ☐ Step 20: Final Service Restart
```bash
sudo systemctl restart sshd
```

### Phase 5: SSL/TLS Setup (Optional but Recommended) (15-30 minutes)

#### ☐ Step 21: Generate Diffie-Hellman Parameters
```bash
# This takes 10-30 minutes on some systems
sudo openssl dhparam -out /etc/nginx/dhparam.pem 4096
```

Run this in the background if needed:
```bash
sudo nohup openssl dhparam -out /etc/nginx/dhparam.pem 4096 &
```

#### ☐ Step 22: Configure Your Domain's DNS
Point your domain to your VPS IP address:
- A record: `yourdomain.com` → `your-vps-ip`
- A record: `www.yourdomain.com` → `your-vps-ip`

Wait for DNS propagation (5-60 minutes)

#### ☐ Step 23: Create Nginx Server Block
```bash
sudo nano /etc/nginx/sites-available/yourdomain.com
```

Basic configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    root /var/www/yourdomain.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # Security headers
    include snippets/security-headers.conf;
}
```

#### ☐ Step 24: Enable Site and Test Nginx
```bash
# Create web root
sudo mkdir -p /var/www/yourdomain.com
echo "Hello World" | sudo tee /var/www/yourdomain.com/index.html

# Enable site
sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

#### ☐ Step 25: Install SSL Certificate with Certbot
```bash
# Install certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Follow the prompts:
# - Enter email address
# - Agree to terms
# - Choose to redirect HTTP to HTTPS (option 2)
```

#### ☐ Step 26: Test Auto-Renewal
```bash
# Test renewal process (doesn't actually renew)
sudo certbot renew --dry-run
```

#### ☐ Step 27: Enable Diffie-Hellman in Nginx SSL Config
```bash
sudo nano /etc/nginx/snippets/ssl-params.conf
```

Uncomment:
```
ssl_dhparam /etc/nginx/dhparam.pem;
```

Reload nginx:
```bash
sudo nginx -t && sudo systemctl reload nginx
```

## Post-Deployment Verification

### ☐ Security Verification Checklist

#### Firewall
```bash
sudo ufw status verbose

# Should show:
# ✓ Default: deny (incoming), allow (outgoing)
# ✓ SSH port allowed
# ✓ Ports 80, 443 allowed
# ✓ Status: active
```

#### SSH Hardening
```bash
sudo sshd -t  # Should show no errors
sudo grep -E "PermitRootLogin|PasswordAuthentication" /etc/ssh/sshd_config.d/99-hardening.conf

# Should show:
# ✓ PermitRootLogin no
# ✓ PasswordAuthentication no
```

#### 2FA
```bash
# From new terminal, should require:
# ✓ SSH key
# ✓ 2FA code from Google Authenticator
```

#### Fail2Ban
```bash
sudo fail2ban-client status

# Should show active jails:
# ✓ sshd
# ✓ nginx-http-auth
# ✓ nginx-noscript
# ✓ nginx-badbots
# ✓ nginx-noproxy
```

#### Automatic Updates
```bash
sudo systemctl status unattended-upgrades

# Should show:
# ✓ Active (running)
```

#### Nginx Security
```bash
curl -I http://yourdomain.com

# Should show headers:
# ✓ X-Frame-Options
# ✓ X-Content-Type-Options
# ✓ X-XSS-Protection
# ✓ No server version disclosure
```

#### SSL/TLS (if configured)
```bash
# Test SSL with SSL Labs:
# https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com
# Should get A+ rating
```

## Maintenance Schedule

### Daily
- [ ] Check fail2ban bans: `sudo fail2ban-client status sshd`
- [ ] Review auth logs: `sudo journalctl -u sshd --since today | grep Failed`

### Weekly
- [ ] Check for pending updates: `apt list --upgradable`
- [ ] Review ufw logs: `sudo less /var/log/ufw.log`
- [ ] Check disk space: `df -h`

### Monthly
- [ ] Rotate emergency codes (generate new ones)
- [ ] Review fail2ban banned IPs
- [ ] Test backup restoration process
- [ ] Review nginx access logs for suspicious activity
- [ ] Update packages manually: `sudo apt update && sudo apt upgrade`

### Quarterly
- [ ] Review and update security configurations
- [ ] Test emergency recovery procedures
- [ ] Audit user accounts and remove unused ones
- [ ] Review and update firewall rules
- [ ] Check SSL certificate expiration (should auto-renew)

## Emergency Contacts

**Keep this information in a secure location:**

```
VPS Provider: _______________
Support URL: _______________
Console Access URL: _______________

Server IP: _______________
SSH Port: _______________
Main Username: _______________

2FA Emergency Codes: (in password manager)
SSH Key Location: _______________

Last Updated: _______________
```

## Rollback Plan

If something goes wrong:

1. **Access via provider console** (not SSH)
2. **Disable 2FA temporarily:**
   ```bash
   sudo sed -i 's/^auth required pam_google_authenticator/#auth required pam_google_authenticator/' /etc/pam.d/sshd
   sudo systemctl restart sshd
   ```
3. **Restore from backup** (if needed)
4. **Review logs:** `sudo journalctl -u sshd -n 100`

## Success Criteria

- [ ] ✅ UFW firewall active with correct rules
- [ ] ✅ SSH only accessible via key + 2FA
- [ ] ✅ Root login disabled
- [ ] ✅ Password authentication disabled
- [ ] ✅ Fail2Ban protecting SSH and Nginx
- [ ] ✅ Automatic security updates enabled
- [ ] ✅ Nginx secured with headers and SSL
- [ ] ✅ SSL certificate installed and auto-renewing
- [ ] ✅ Emergency codes backed up in 2+ locations
- [ ] ✅ Can successfully log in from new terminal
- [ ] ✅ Provider console access verified
- [ ] ✅ All services running without errors

## Additional Resources

- Full 2FA Guide: `2fa_setup_guide.md`
- Emergency Recovery: `emergency_recovery.md`
- Security Script: `vps_security_hardening.sh`

---

**Total Estimated Time: 1.5 - 2 hours**

**Recommended: Do this during a maintenance window when downtime is acceptable**
