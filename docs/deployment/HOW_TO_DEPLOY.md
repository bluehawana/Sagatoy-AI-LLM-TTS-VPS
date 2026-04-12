# How to Deploy VPS Security

## ⚡ Super Quick Method (One Script)

### Step 1: Upload the Script to Your VPS

**Option A: Using SCP (from your local machine)**
```bash
scp secure_vps.sh your-user@your-vps-ip:/tmp/
```

**Option B: Using nano directly on VPS**
```bash
# SSH to your VPS
ssh your-user@your-vps-ip

# Create the script
nano /tmp/secure_vps.sh

# Paste the entire contents of secure_vps.sh
# Save with Ctrl+X, then Y, then Enter
```

**Option C: Using wget/curl (if you host it somewhere)**
```bash
# On your VPS
wget -O /tmp/secure_vps.sh https://your-url/secure_vps.sh
# or
curl -o /tmp/secure_vps.sh https://your-url/secure_vps.sh
```

### Step 2: Review the Script (IMPORTANT!)
```bash
# Always review scripts before running them!
nano /tmp/secure_vps.sh

# Or use less to read it
less /tmp/secure_vps.sh
```

### Step 3: Make it Executable
```bash
chmod +x /tmp/secure_vps.sh
```

### Step 4: Run the Script
```bash
sudo /tmp/secure_vps.sh
```

The script will:
- ✅ Ask you questions interactively
- ✅ Confirm each step
- ✅ Back up existing configurations
- ✅ Configure everything automatically
- ✅ Give you clear instructions for 2FA setup

### Step 5: Follow the 2FA Instructions

After the script completes, it will show you exactly what to do for 2FA setup.

**Quick 2FA setup:**
```bash
# 1. Switch to your user
su - yourusername

# 2. Run Google Authenticator
google-authenticator
# Answer: y, y, n, y
# SAVE THE EMERGENCY CODES!
# Scan QR code with your phone

# 3. Exit back to root
exit

# 4. Run the helper script
sudo /root/setup_2fa_step2.sh

# 5. TEST IN NEW TERMINAL!
# (keep current session open)
```

## 🔍 What the Script Does

The `secure_vps.sh` script is **interactive** and will:

1. **Check prerequisites** - Ensures you have backups and console access
2. **Ask about settings** - SSH port, username, additional firewall rules
3. **Create/configure user** - Non-root user with sudo access
4. **Set up firewall** - UFW with strict rules
5. **Harden SSH** - Disable root, strong ciphers, security settings
6. **Configure Fail2Ban** - Auto-ban brute force attempts
7. **Enable auto-updates** - Security patches applied automatically
8. **Secure Nginx** - Security headers and SSL config (if installed)
9. **Guide 2FA setup** - Step-by-step instructions for Google Authenticator

## ⚠️ Safety Features

The script includes:
- ✅ Configuration backups before any changes
- ✅ Validation of SSH config before restarting
- ✅ Confirmation prompts for critical actions
- ✅ Colored output for easy reading
- ✅ Detailed error messages
- ✅ Rollback instructions if needed

## 📝 Example Run

```
$ sudo /tmp/secure_vps.sh

========================================
VPS Security Hardening Script
========================================

This script will secure your VPS with:
  • UFW Firewall with strict rules
  • SSH hardening (disabled root, strong ciphers)
  • Two-Factor Authentication (2FA) setup
  • Fail2Ban intrusion prevention
  • Automatic security updates
  • Nginx security configurations

⚠ BEFORE CONTINUING, ENSURE YOU HAVE:
  1. Created a VPS snapshot/backup
  2. Console access via your VPS provider's dashboard
  3. Google Authenticator app installed on your phone
  4. Keep this SSH session open during the entire process

Have you completed all the above requirements? [y/n]: y

ℹ Current SSH port: 22
Do you want to change the SSH port? (Recommended for security) [y/n]: y
Enter new SSH port (1024-65535): 2222
✓ SSH port will be changed to: 2222

ℹ You should NOT use root for SSH access.
Enter the username you'll use for SSH (or create new): myuser

... (continues interactively)
```

## 🚨 Important Safety Notes

### BEFORE Running the Script

1. **Create a VPS snapshot/backup** through your provider's dashboard
   - DigitalOcean: Droplet → Snapshots
   - Linode: Linode → Backups
   - AWS: EC2 → Create Snapshot
   - Vultr: Server → Snapshots
   - Hetzner: Server → Snapshots

2. **Verify console access**
   - Know how to access your VPS console via web interface
   - This is your emergency access if SSH breaks

3. **Have Google Authenticator ready**
   - Install on your phone before starting
   - iOS: App Store
   - Android: Google Play Store

### DURING Execution

1. **Keep your current SSH session open**
   - Don't close it until testing is complete
   - Test new connections in a SEPARATE terminal

2. **Read each prompt carefully**
   - The script asks for confirmation on critical steps
   - Take your time to understand what's happening

3. **Save the emergency 2FA codes**
   - When you run `google-authenticator`, you'll get backup codes
   - **Save these in a password manager IMMEDIATELY**
   - They're your backup if you lose your phone

### AFTER Execution

1. **Test SSH in a NEW terminal**
   ```bash
   ssh myuser@your-vps-ip -p 2222
   ```
   - You should be prompted for your 2FA code
   - Enter the 6-digit code from Google Authenticator

2. **Verify everything works**
   - Can log in with SSH key + 2FA ✓
   - Cannot log in with wrong 2FA code ✓
   - Sudo access works ✓

3. **Only then close your original session**

## 🔧 Customization

You can edit the script before running to customize:

```bash
nano /tmp/secure_vps.sh
```

**Common customizations:**
- Default SSH port (line ~199)
- Fail2Ban ban time (line ~441)
- Firewall rules (lines ~317-343)
- Nginx configurations (lines ~508-583)

## 🆘 If Something Goes Wrong

### Can't SSH after running script

1. **Use your VPS provider's web console** (not SSH)
2. **Check if SSH is running:**
   ```bash
   sudo systemctl status sshd
   ```
3. **Check if UFW blocked you:**
   ```bash
   sudo ufw status
   sudo ufw allow 22/tcp  # or your SSH port
   ```
4. **Restore from backup:**
   ```bash
   # Find your backup
   ls /root/security_backups_*

   # Restore SSH config
   sudo cp /root/security_backups_*/sshd_config.bak /etc/ssh/sshd_config
   sudo systemctl restart sshd
   ```

### 2FA not working

1. **Access via console**
2. **Disable 2FA temporarily:**
   ```bash
   sudo nano /etc/pam.d/sshd
   # Comment out the pam_google_authenticator line
   # auth required pam_google_authenticator.so nullok

   sudo systemctl restart sshd
   ```
3. **Fix the issue, then re-enable**

### Script failed partway through

The script uses `set -e` which means it stops on first error.

1. **Check what failed:**
   - Read the error message carefully
   - It will show which line failed

2. **Fix the issue:**
   - Usually a missing package or permission issue

3. **Re-run the script:**
   - It's designed to be idempotent (safe to run multiple times)
   - It will skip steps that are already done

## 📊 Verification After Setup

Run these commands to verify everything is secure:

```bash
# Check firewall
sudo ufw status verbose

# Check Fail2Ban
sudo fail2ban-client status

# Check SSH config
sudo sshd -t

# Check what's listening on ports
sudo netstat -tulpn

# Check failed login attempts
sudo journalctl -u sshd | grep Failed

# Check Fail2Ban bans
sudo fail2ban-client status sshd
```

## 🎯 What You'll Have After

Once complete, your VPS will have:

✅ **Firewall**: Only SSH (custom port), HTTP, and HTTPS open
✅ **SSH**: Requires both your SSH key AND your phone (2FA)
✅ **No root login**: Can't SSH as root anymore
✅ **No password auth**: Only SSH keys work (after 2FA enabled)
✅ **Auto-defense**: Fail2Ban auto-bans brute force attempts
✅ **Auto-updates**: Security patches installed automatically
✅ **Secure web**: Nginx with security headers (if installed)
✅ **Monitoring**: All failed login attempts logged

## 📚 Files Created by Script

- `/root/security_backups_[timestamp]/` - Backup of original configs
- `/etc/ssh/sshd_config.d/99-hardening.conf` - SSH hardening settings
- `/etc/fail2ban/jail.local` - Fail2Ban configuration
- `/etc/nginx/snippets/security-headers.conf` - Nginx security headers
- `/etc/nginx/snippets/ssl-params.conf` - SSL/TLS configuration
- `/root/setup_2fa_step2.sh` - Helper script for 2FA setup

## 🔄 Maintenance

### Daily
```bash
# Check for attacks
sudo fail2ban-client status sshd
```

### Weekly
```bash
# Check for updates
apt list --upgradable
```

### Monthly
```bash
# Refresh 2FA emergency codes
google-authenticator

# Manual system update
sudo apt update && sudo apt upgrade
```

## ✅ Checklist

Before running:
- [ ] Created VPS snapshot/backup
- [ ] Verified console access works
- [ ] Installed Google Authenticator app
- [ ] Have 1-2 hours uninterrupted time

During setup:
- [ ] Reviewed the script with `nano` or `less`
- [ ] Keep current SSH session open
- [ ] Saved 2FA emergency codes

After setup:
- [ ] Tested SSH in new terminal
- [ ] 2FA working correctly
- [ ] Emergency codes saved securely
- [ ] Know how to access console if locked out

---

**Ready to deploy?**

```bash
sudo /tmp/secure_vps.sh
```

**Good luck! Your VPS will be Fort Knox when you're done! 🛡️**
