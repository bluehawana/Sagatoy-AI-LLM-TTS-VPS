# Google Authenticator 2FA Setup Guide

This guide will help you set up Two-Factor Authentication (2FA) for SSH access to your VPS, ensuring only you can log in.

## Prerequisites

- SSH access to your VPS
- A smartphone with Google Authenticator app installed
  - iOS: https://apps.apple.com/app/google-authenticator/id388497605
  - Android: https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2
- **IMPORTANT**: Keep your current SSH session open during setup!

## Setup Steps

### Step 1: Create a Non-Root User (if not already done)

```bash
# Create a new user (replace 'yourusername' with your desired username)
sudo adduser yourusername

# Add user to sudo group
sudo usermod -aG sudo yourusername

# Copy SSH keys to new user (if using key-based auth)
sudo mkdir -p /home/yourusername/.ssh
sudo cp ~/.ssh/authorized_keys /home/yourusername/.ssh/
sudo chown -R yourusername:yourusername /home/yourusername/.ssh
sudo chmod 700 /home/yourusername/.ssh
sudo chmod 600 /home/yourusername/.ssh/authorized_keys
```

### Step 2: Configure Google Authenticator for Your User

**Switch to your non-root user:**
```bash
su - yourusername
```

**Run the Google Authenticator setup:**
```bash
google-authenticator
```

**Answer the prompts as follows:**

1. **"Do you want authentication tokens to be time-based?"**
   - Answer: `y` (yes)
   - A QR code will be displayed

2. **IMPORTANT: Save Your Emergency Codes!**
   - You'll see several emergency scratch codes
   - **SAVE THESE IN A SECURE LOCATION** (password manager, encrypted file, etc.)
   - These are your backup if you lose your phone!

3. **Scan the QR code with Google Authenticator app:**
   - Open Google Authenticator on your phone
   - Tap the "+" button
   - Choose "Scan a QR code"
   - Scan the QR code displayed in your terminal

4. **"Do you want me to update your ~/.google_authenticator file?"**
   - Answer: `y` (yes)

5. **"Do you want to disallow multiple uses of the same authentication token?"**
   - Answer: `y` (yes) - Prevents replay attacks

6. **"By default, tokens are good for 30 seconds... Do you want to increase the time window?"**
   - Answer: `n` (no) - Keep it at 30 seconds for maximum security

7. **"Do you want to enable rate-limiting?"**
   - Answer: `y` (yes) - Limits brute force attacks to 3 attempts per 30 seconds

### Step 3: Configure PAM (Pluggable Authentication Modules)

**Edit the SSH PAM configuration:**
```bash
sudo nano /etc/pam.d/sshd
```

**Add this line at the TOP of the file:**
```
auth required pam_google_authenticator.so nullok
```

The `nullok` option allows users without 2FA to still log in (remove this later after all users have 2FA set up).

**Comment out or remove this line (to prevent challenge-response conflicts):**
```
# @include common-auth
```

**Save and exit** (Ctrl+X, then Y, then Enter)

### Step 4: Configure SSH to Use 2FA

**Edit SSH daemon configuration:**
```bash
sudo nano /etc/ssh/sshd_config
```

**Add or modify these lines:**
```
ChallengeResponseAuthentication yes
UsePAM yes

# For key + 2FA (most secure - requires both SSH key AND 2FA code)
AuthenticationMethods publickey,keyboard-interactive

# Alternative: For password + 2FA (if not using SSH keys)
# AuthenticationMethods keyboard-interactive
```

**Save and exit** (Ctrl+X, then Y, then Enter)

### Step 5: Restart SSH Service

**IMPORTANT: DO NOT close your current SSH session!**

```bash
# Test the SSH configuration first
sudo sshd -t

# If test passes, restart SSH
sudo systemctl restart sshd
```

### Step 6: Test 2FA Login

**Open a NEW terminal window** (keep your current session open!)

Try to log in:
```bash
ssh yourusername@your-vps-ip
```

You should be prompted for:
1. Your SSH key passphrase (if using keys)
2. Your 2FA verification code from Google Authenticator

**Do not close your original session until you confirm the new login works!**

## Hardening Further: Disable Password Authentication

Once 2FA is working, disable password authentication:

```bash
sudo nano /etc/ssh/sshd_config.d/99-hardening.conf
```

Uncomment this line:
```
PasswordAuthentication no
```

Restart SSH:
```bash
sudo systemctl restart sshd
```

## Security Best Practices

### 1. Save Your Emergency Codes
- Store emergency scratch codes in a password manager (1Password, Bitwarden, etc.)
- Keep a printed copy in a secure physical location
- Never share these codes or take screenshots

### 2. Backup Your 2FA Secret
The secret key is stored in: `~/.google_authenticator`

**Backup this file securely:**
```bash
# Create encrypted backup
gpg -c ~/.google_authenticator
# This creates ~/.google_authenticator.gpg (encrypted with a password)
```

### 3. Multiple Users
Each user needs to run `google-authenticator` separately for their own account.

### 4. Remove the 'nullok' Option
After all users have 2FA set up, remove `nullok` from `/etc/pam.d/sshd`:
```bash
sudo nano /etc/pam.d/sshd
# Change this:
auth required pam_google_authenticator.so nullok
# To this:
auth required pam_google_authenticator.so
```

## Troubleshooting

### Can't Log In After Enabling 2FA

**If you get locked out:**

1. **Use your VPS provider's console access** (not SSH)
   - Most VPS providers (DigitalOcean, Linode, AWS, etc.) have a web-based console

2. **Disable 2FA temporarily:**
   ```bash
   sudo nano /etc/pam.d/sshd
   # Comment out the line:
   # auth required pam_google_authenticator.so

   sudo systemctl restart sshd
   ```

3. **Fix the issue, then re-enable**

### Using Emergency Codes

If you lose your phone, use one of your emergency scratch codes instead of the 6-digit code from Google Authenticator.

**After using an emergency code, generate new ones:**
```bash
google-authenticator
```

### Time Synchronization Issues

If codes don't work, your server time might be wrong:
```bash
# Install NTP
sudo apt install -y ntp

# Check time
date

# Sync time
sudo ntpdate -s time.nist.gov
```

## Recovery Options

### Option 1: Provider Console Access
All VPS providers offer console access through their web dashboard. This bypasses SSH entirely.

### Option 2: Rescue Mode
Most providers offer a rescue/recovery mode that lets you boot from a recovery image and access your files.

### Option 3: Keep a Backup 2FA Device
Set up Google Authenticator on multiple devices (tablet, old phone, etc.) as backup.

## Testing Your Setup

**Test that everything works:**

1. ✅ Can log in with SSH key + 2FA code
2. ✅ Cannot log in with wrong 2FA code
3. ✅ Emergency codes work
4. ✅ Fail2Ban is active: `sudo fail2ban-client status sshd`
5. ✅ UFW firewall is active: `sudo ufw status`

## Additional Security: IP Whitelisting (Optional)

If you have a static IP, you can whitelist only your IP:

```bash
# Edit fail2ban
sudo nano /etc/fail2ban/jail.local

# Add your IP to ignoreip
ignoreip = 127.0.0.1/8 ::1 YOUR.IP.ADDRESS.HERE
```

**Or restrict SSH to specific IPs in UFW:**
```bash
# Remove the general SSH rule
sudo ufw delete allow 22/tcp

# Add IP-specific rule (replace YOUR_IP)
sudo ufw allow from YOUR_IP to any port 22 proto tcp comment 'SSH from my IP only'
```

---

## Quick Reference Card

**Login Process:**
1. SSH to server: `ssh yourusername@server-ip`
2. Enter SSH key passphrase (if you have one)
3. Enter 6-digit code from Google Authenticator app
4. You're in! 🎉

**Emergency Scratch Codes:**
- Location: Stored when you ran `google-authenticator`
- Use once instead of the 6-digit code if you lose your phone

**Important Files:**
- `~/.google_authenticator` - Your 2FA secret (backup this file!)
- `/etc/pam.d/sshd` - PAM configuration
- `/etc/ssh/sshd_config` - SSH configuration

**Important Commands:**
- Test SSH config: `sudo sshd -t`
- Restart SSH: `sudo systemctl restart sshd`
- Check SSH status: `sudo systemctl status sshd`
- View failed login attempts: `sudo journalctl -u sshd | grep Failed`
