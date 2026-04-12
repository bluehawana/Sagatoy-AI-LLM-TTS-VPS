# Emergency Recovery & Troubleshooting Guide

## If You Get Locked Out

### Method 1: VPS Provider Console Access (Recommended)

All VPS providers offer console/terminal access through their web dashboard. This is your primary recovery method.

#### DigitalOcean
1. Log into your DigitalOcean dashboard
2. Click on your Droplet
3. Click "Access" → "Launch Droplet Console"
4. Log in with your username and password

#### Linode
1. Log into Linode Manager
2. Select your Linode
3. Click "Launch LISH Console"
4. Log in with your username and password

#### AWS EC2
1. Log into AWS Console
2. Navigate to EC2 → Instances
3. Select your instance → "Connect" → "EC2 Instance Connect"

#### Vultr
1. Log into Vultr dashboard
2. Click on your server
3. Click "View Console"

#### Hetzner
1. Log into Hetzner Cloud Console
2. Select your server
3. Click "Console" button

### Method 2: Disable 2FA Temporarily

Once you have console access:

```bash
# Log in with username and password through console

# Disable 2FA in PAM
sudo nano /etc/pam.d/sshd

# Comment out this line:
# auth required pam_google_authenticator.so nullok

# Save and exit (Ctrl+X, Y, Enter)

# Restart SSH
sudo systemctl restart sshd

# Now you can SSH without 2FA
# Fix your issue, then re-enable 2FA
```

### Method 3: Rescue Mode

Most VPS providers offer a rescue/recovery mode:

1. **Enable Rescue Mode** through your provider's dashboard
2. **Boot into rescue environment**
3. **Mount your file system:**
   ```bash
   # Usually something like:
   mount /dev/vda1 /mnt

   # Edit the PAM configuration
   nano /mnt/etc/pam.d/sshd

   # Comment out the 2FA line
   # auth required pam_google_authenticator.so

   # Save and reboot normally
   ```

## Common Issues & Solutions

### Issue 1: "Permission denied (publickey,keyboard-interactive)"

**Cause:** 2FA is required but not working

**Solution:**
```bash
# Check PAM configuration
sudo cat /etc/pam.d/sshd | grep google-authenticator

# Verify Google Authenticator file exists
ls -la ~/.google_authenticator

# Check file permissions
chmod 400 ~/.google_authenticator

# Check SSH logs for errors
sudo journalctl -u sshd -n 50
```

### Issue 2: "Verification code is incorrect" (but you know it's right)

**Cause:** Server time is out of sync

**Solution:**
```bash
# Check current time
date

# Install NTP if not present
sudo apt install -y ntp

# Synchronize time
sudo systemctl stop ntp
sudo ntpdate -s time.nist.gov
sudo systemctl start ntp

# Verify time is correct
date
```

### Issue 3: Lost Phone / Can't Access Google Authenticator

**Solution 1: Use Emergency Scratch Codes**
- You saved these when setting up 2FA (right?)
- Use one of those codes instead of the 6-digit code
- Each code can only be used once

**Solution 2: Access via Console**
```bash
# Log in through provider's console
# Generate new codes
google-authenticator

# Save the new emergency codes
# Scan the new QR code with your new device
```

### Issue 4: Accidentally Locked Out Root User

**Solution:**
```bash
# Access via console
# Create/use a non-root user with sudo access
sudo adduser recoveryuser
sudo usermod -aG sudo recoveryuser

# Set up SSH keys for new user
sudo mkdir -p /home/recoveryuser/.ssh
sudo cp ~/.ssh/authorized_keys /home/recoveryuser/.ssh/
sudo chown -R recoveryuser:recoveryuser /home/recoveryuser/.ssh
sudo chmod 700 /home/recoveryuser/.ssh
sudo chmod 600 /home/recoveryuser/.ssh/authorized_keys
```

### Issue 5: UFW Locked Me Out

**Cause:** Firewall rules blocked SSH before you could test

**Solution via Console:**
```bash
# Disable UFW temporarily
sudo ufw disable

# Or allow your current IP
sudo ufw allow from YOUR_IP to any port 22

# Re-enable UFW
sudo ufw enable

# Check status
sudo ufw status verbose
```

### Issue 6: Fail2Ban Banned My IP

**Check if you're banned:**
```bash
sudo fail2ban-client status sshd
```

**Unban yourself:**
```bash
# Replace YOUR_IP with your actual IP
sudo fail2ban-client set sshd unbanip YOUR_IP

# Or temporarily stop Fail2Ban
sudo systemctl stop fail2ban
```

### Issue 7: SSH Won't Start After Configuration Changes

**Check configuration errors:**
```bash
# Test SSH configuration
sudo sshd -t

# If there are errors, fix them in the config files

# Check SSH service status
sudo systemctl status sshd

# View detailed logs
sudo journalctl -u sshd -n 100 --no-pager
```

## Prevention: Before Making Changes

### 1. Always Keep a Session Open
```bash
# When making SSH changes, always:
# 1. Keep your current SSH session open
# 2. Open a NEW terminal to test
# 3. Only close the original after confirming new login works
```

### 2. Create a Recovery User
```bash
# Create a backup user with sudo access
sudo adduser backupadmin
sudo usermod -aG sudo backupadmin
sudo passwd backupadmin  # Set a strong password

# Copy SSH keys
sudo mkdir -p /home/backupadmin/.ssh
sudo cp ~/.ssh/authorized_keys /home/backupadmin/.ssh/
sudo chown -R backupadmin:backupadmin /home/backupadmin/.ssh
sudo chmod 700 /home/backupadmin/.ssh
sudo chmod 600 /home/backupadmin/.ssh/authorized_keys

# DO NOT enable 2FA for this user initially (it's your backup)
```

### 3. Document Your Setup
```bash
# Keep a record of:
# - Your VPS provider's console access method
# - Your emergency scratch codes (in password manager)
# - Which users have 2FA enabled
# - Current SSH port
# - Backup authentication methods
```

### 4. Test Before Finalizing
```bash
# Test checklist:
# ✅ Can log in from new terminal
# ✅ 2FA codes work
# ✅ Emergency codes work (test one)
# ✅ SSH keys work
# ✅ Sudo access works
# ✅ Firewall allows SSH
# ✅ Know how to access provider console
```

## Rollback Procedures

### Rollback SSH Configuration

```bash
# Your original config was backed up to:
# /root/security_backups_TIMESTAMP/sshd_config.bak

# Restore it:
sudo cp /root/security_backups_*/sshd_config.bak /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### Rollback 2FA

```bash
# Disable in PAM
sudo nano /etc/pam.d/sshd
# Comment out: auth required pam_google_authenticator.so

# Restore SSH config
sudo nano /etc/ssh/sshd_config
# Change back to:
ChallengeResponseAuthentication no
# Or remove AuthenticationMethods line

sudo systemctl restart sshd
```

### Rollback Firewall

```bash
# Disable UFW completely
sudo ufw disable

# Or reset to defaults
sudo ufw --force reset
sudo ufw allow 22/tcp
sudo ufw enable
```

## Emergency Contact Info Template

Save this information in a secure location:

```
VPS EMERGENCY INFO
==================

Provider: _______________
Account Email: _______________
Account Password Location: _______________

Server IP: _______________
SSH Port: _______________
SSH Username: _______________

Console Access URL: _______________
Provider Support: _______________

2FA Emergency Codes Location: _______________
SSH Key Location: _______________
SSH Key Passphrase Location: _______________

Backup User: _______________
Backup User Password Location: _______________

Last Backup Date: _______________
Backup Location: _______________
```

## Testing Your Recovery Plan

**Do this BEFORE you need it:**

1. **Test console access:**
   - Log into your VPS provider dashboard
   - Open the console
   - Verify you can log in

2. **Test emergency codes:**
   - Try logging in with one emergency scratch code
   - Verify it works
   - Generate new codes afterward

3. **Test backup user:**
   - Try logging in as your backup user
   - Verify sudo access works

4. **Document the process:**
   - Write down the steps you took
   - Save screenshots of console access
   - Store in password manager or secure location

## Quick Recovery Commands

**Disable 2FA (via console):**
```bash
sudo sed -i 's/^auth required pam_google_authenticator/#auth required pam_google_authenticator/' /etc/pam.d/sshd && sudo systemctl restart sshd
```

**Disable UFW:**
```bash
sudo ufw disable
```

**Unban yourself from Fail2Ban:**
```bash
sudo fail2ban-client set sshd unbanip $(echo $SSH_CLIENT | awk '{print $1}')
```

**Emergency: Allow all SSH connections:**
```bash
sudo ufw allow 22/tcp && sudo systemctl restart sshd
```

---

**Remember:** The best recovery is prevention. Always test changes in a new terminal while keeping your original session open!
