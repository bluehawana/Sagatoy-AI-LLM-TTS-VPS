# VPS Security Hardening Suite

Complete security hardening solution for your VPS with 2FA authentication.

## 🎯 Overview

This security suite transforms your VPS into a fortress with:
- **Two-Factor Authentication (2FA)** - Only you can access
- **Hardened SSH** - Key-based + 2FA required
- **Firewall Protection** - UFW with strict rules
- **Intrusion Prevention** - Fail2Ban auto-banning
- **Automatic Updates** - Security patches applied automatically
- **SSL/TLS** - A+ rating HTTPS configuration
- **Security Headers** - Protection against XSS, clickjacking, etc.

## 📁 Files in This Suite

| File | Purpose | When to Use |
|------|---------|-------------|
| **QUICK_START.md** | Fast-track setup guide | Start here if experienced |
| **SECURITY_DEPLOYMENT_CHECKLIST.md** | Complete step-by-step checklist | Detailed deployment guide |
| **vps_security_hardening.sh** | Main security script | Run on VPS to configure everything |
| **2fa_setup_guide.md** | 2FA configuration guide | Setting up Google Authenticator |
| **emergency_recovery.md** | Lockout recovery procedures | If you get locked out |

## 🚀 Quick Start

### For Experienced Users (1.5 hours)

```bash
# 1. Upload security script to your VPS
scp vps_security_hardening.sh your-user@your-vps:/tmp/

# 2. SSH to VPS and run script
ssh your-user@your-vps
sudo bash /tmp/vps_security_hardening.sh

# 3. Set up 2FA - Follow prompts in 2fa_setup_guide.md
google-authenticator

# 4. Test everything
# See QUICK_START.md for detailed steps
```

**→ See [QUICK_START.md](QUICK_START.md) for complete fast-track guide**

### For Beginners or Methodical Approach (2 hours)

**→ See [SECURITY_DEPLOYMENT_CHECKLIST.md](SECURITY_DEPLOYMENT_CHECKLIST.md)**

This provides a complete checklist with verification steps at each stage.

## 🔐 What Gets Secured

### 1. SSH Access
- ✅ Two-Factor Authentication (2FA) required
- ✅ SSH key authentication required
- ✅ Password authentication disabled
- ✅ Root login disabled
- ✅ Strong ciphers only
- ✅ Rate limiting enabled
- ✅ Login attempts logged

**Result:** Only you can log in, using your SSH key + phone

### 2. Firewall (UFW)
- ✅ Default deny incoming
- ✅ Only SSH, HTTP, HTTPS allowed
- ✅ Configurable per-IP rules
- ✅ Logging enabled

**Result:** All ports blocked except what you explicitly allow

### 3. Intrusion Prevention (Fail2Ban)
- ✅ Auto-ban after 3 failed SSH attempts
- ✅ Protection for Nginx endpoints
- ✅ Bot detection and blocking
- ✅ Customizable ban times

**Result:** Brute force attacks automatically blocked

### 4. Web Server (Nginx)
- ✅ Security headers (XSS, clickjacking protection)
- ✅ TLS 1.2 and 1.3 only
- ✅ Strong cipher suites
- ✅ OCSP stapling
- ✅ Server version hidden

**Result:** A+ rating on SSL Labs

### 5. System Updates
- ✅ Automatic security updates
- ✅ Daily update checks
- ✅ Auto-cleanup of old packages
- ✅ Optional auto-reboot

**Result:** Always protected against known vulnerabilities

## 📋 Prerequisites

Before starting, ensure you have:

- [ ] Root or sudo access to your VPS
- [ ] SSH key-based authentication set up
- [ ] Google Authenticator app on your phone
- [ ] Backup/snapshot of your VPS created
- [ ] Access to your VPS provider's web console
- [ ] 1.5-2 hours of uninterrupted time

## ⚠️ Critical Safety Information

### BEFORE Running Anything

1. **Create a snapshot/backup** of your VPS
2. **Verify console access** through your provider's dashboard
3. **Keep your current SSH session open** while testing changes
4. **Test in a NEW terminal** before closing original session

### Emergency Access

If you get locked out:
1. Use your VPS provider's web console (not SSH)
2. Follow recovery steps in [emergency_recovery.md](emergency_recovery.md)
3. Your emergency 2FA codes are your backup

## 📖 Detailed Guides

### 2FA Setup
**File:** [2fa_setup_guide.md](2fa_setup_guide.md)

Complete guide for setting up Two-Factor Authentication:
- Google Authenticator setup
- PAM configuration
- SSH configuration
- Testing procedures
- Emergency codes
- Recovery options

### Emergency Recovery
**File:** [emergency_recovery.md](emergency_recovery.md)

What to do if:
- You get locked out
- Lost your phone
- 2FA not working
- Firewall blocked you
- Fail2Ban banned you
- SSH won't start

### Deployment Checklist
**File:** [SECURITY_DEPLOYMENT_CHECKLIST.md](SECURITY_DEPLOYMENT_CHECKLIST.md)

Step-by-step checklist with:
- Pre-deployment preparation
- Phase-by-phase deployment
- Verification at each step
- Post-deployment testing
- Maintenance schedule

## 🛠️ What the Security Script Does

**File:** [vps_security_hardening.sh](vps_security_hardening.sh)

When you run this script, it automatically:

1. **Backs up** existing configurations
2. **Configures UFW** with strict firewall rules
3. **Hardens SSH** with secure ciphers and settings
4. **Sets up Fail2Ban** with multiple jails
5. **Enables automatic security updates**
6. **Creates Nginx security configurations**
7. **Sets proper file permissions**

**Duration:** 2-5 minutes to run

## 🧪 Testing & Verification

After deployment, verify everything works:

```bash
# Firewall
sudo ufw status verbose

# Fail2Ban
sudo fail2ban-client status

# SSH configuration
sudo sshd -t

# Can log in with 2FA (in NEW terminal!)
ssh your-user@your-vps

# Nginx
sudo nginx -t
curl -I https://yourdomain.com

# Automatic updates
sudo systemctl status unattended-upgrades
```

**Full testing checklist:** See SECURITY_DEPLOYMENT_CHECKLIST.md

## 🔄 Maintenance

### Daily
```bash
# Check for suspicious activity
sudo journalctl -u sshd --since today | grep Failed
sudo fail2ban-client status sshd
```

### Weekly
```bash
# Check for updates
apt list --upgradable

# Review logs
sudo tail -100 /var/log/auth.log
```

### Monthly
```bash
# Generate new 2FA emergency codes
google-authenticator

# Manual system update
sudo apt update && sudo apt upgrade
```

## 🆘 Support & Resources

### If You Get Locked Out
1. **Don't panic!** Access via provider's web console
2. See [emergency_recovery.md](emergency_recovery.md)
3. Use your emergency scratch codes

### If Services Fail
```bash
# Check service status
sudo systemctl status sshd fail2ban nginx

# View logs
sudo journalctl -u sshd -n 50
sudo journalctl -u fail2ban -n 50

# Restart services
sudo systemctl restart sshd
```

### Common Issues

**"Verification code is incorrect"**
- Server time might be wrong: `sudo ntpdate -s time.nist.gov`

**Locked out after 2FA**
- Use provider console, disable 2FA temporarily (see emergency_recovery.md)

**Firewall blocking SSH**
- Use provider console: `sudo ufw allow 22/tcp`

## 🎯 Security Levels Achieved

| Component | Rating | Details |
|-----------|--------|---------|
| SSH Access | ⭐⭐⭐⭐⭐ | Key + 2FA + hardened config |
| Firewall | ⭐⭐⭐⭐⭐ | Strict rules, minimal exposure |
| Intrusion Prevention | ⭐⭐⭐⭐⭐ | Auto-banning active |
| Web Security | ⭐⭐⭐⭐⭐ | Security headers + SSL |
| Updates | ⭐⭐⭐⭐⭐ | Automatic security patches |

**Overall Security:** Military-grade 🛡️

## 📊 Comparison: Before vs After

### Before This Setup
- ❌ Password-based SSH (easily brute-forced)
- ❌ Root login allowed (common target)
- ❌ No firewall (all ports exposed)
- ❌ No intrusion prevention
- ❌ Manual updates (vulnerabilities linger)
- ❌ No SSL (data transmitted in clear text)
- ❌ Weak SSH ciphers (potentially crackable)

### After This Setup
- ✅ SSH key + 2FA required (nearly impossible to breach)
- ✅ Root login disabled (attack surface reduced)
- ✅ Firewall active (only necessary ports open)
- ✅ Fail2Ban blocking attacks (auto-defense)
- ✅ Automatic security updates (always protected)
- ✅ SSL with A+ rating (encrypted connections)
- ✅ Strong ciphers only (military-grade encryption)

## 🎓 Educational Resources

### Understanding the Components

**UFW (Uncomplicated Firewall)**
- Blocks all incoming traffic by default
- Allows only specific ports you define
- Logs all blocked attempts

**Fail2Ban**
- Monitors log files for suspicious activity
- Automatically bans IPs after failed attempts
- Prevents brute force attacks

**2FA (Two-Factor Authentication)**
- "Something you have" (phone) + "Something you know" (SSH key)
- Even if SSH key is stolen, attacker needs your phone
- Time-based codes change every 30 seconds

**SSH Hardening**
- Disables weak ciphers and protocols
- Prevents common attack vectors
- Limits authentication attempts

### Security Best Practices

1. **Never share your SSH private key**
2. **Store emergency codes in password manager**
3. **Keep your local machine secure** (if it's compromised, SSH keys are too)
4. **Use strong passphrases** on SSH keys
5. **Regularly review logs** for suspicious activity
6. **Keep systems updated**
7. **Use separate keys** for different servers
8. **Enable 2FA on everything** (email, GitHub, VPS provider, etc.)

## 🚨 Warning Signs

Monitor for these and investigate immediately:

```bash
# Unusual number of failed login attempts
sudo journalctl -u sshd | grep Failed | wc -l

# Unknown IPs in Fail2Ban bans
sudo fail2ban-client status sshd

# Unexpected processes
ps aux | grep -v root

# Unusual network connections
sudo netstat -tulpn

# File modifications you didn't make
sudo find /etc -type f -mtime -1
```

## 📞 Emergency Contacts Template

Save this information in your password manager:

```
VPS SECURITY INFO
=================

Provider: _______________
Console URL: _______________
Support: _______________

Server IP: _______________
SSH Port: _______________
SSH User: _______________

2FA Emergency Codes: [in password manager]
SSH Key: [path on local machine]
Key Passphrase: [in password manager]

Last Security Update: _______________
Last 2FA Code Refresh: _______________
```

## 🎉 Success Criteria

After completing this setup, you should have:

- ✅ Cannot SSH without your private key
- ✅ Cannot SSH without 2FA code from your phone
- ✅ Root login completely disabled
- ✅ Password authentication disabled
- ✅ Firewall blocking all unnecessary ports
- ✅ Fail2Ban auto-banning attackers
- ✅ SSL certificate installed and auto-renewing
- ✅ Automatic security updates enabled
- ✅ Security headers protecting web traffic
- ✅ Emergency recovery plan documented

## 📝 Next Steps

1. **Complete the setup** using QUICK_START.md or SECURITY_DEPLOYMENT_CHECKLIST.md
2. **Test everything** thoroughly
3. **Document your setup** (save emergency codes!)
4. **Set up monitoring** (optional: Netdata, Grafana, etc.)
5. **Schedule regular maintenance** (monthly review)
6. **Consider additional hardening:**
   - IP whitelisting (if static IP)
   - VPN access (WireGuard/OpenVPN)
   - Intrusion detection (AIDE, Tripwire)
   - Log aggregation (ELK stack)

## 📜 License & Disclaimer

These scripts are provided as-is for educational and security hardening purposes.

**Disclaimer:**
- Always test in a safe environment first
- Create backups before making changes
- Keep emergency access methods available
- The authors are not responsible for misconfigurations or lockouts

**Recommended Use:**
- Development VPS: Test first
- Production VPS: Schedule maintenance window
- Always have a backup/snapshot

## 🙏 Credits

Security configurations based on:
- CIS Benchmarks
- NIST Security Guidelines
- OWASP Best Practices
- Ubuntu Security Guide
- Mozilla SSL Configuration Generator

## 📚 Additional Reading

- [CIS Ubuntu Linux Benchmark](https://www.cisecurity.org/benchmark/ubuntu_linux)
- [SSH Hardening Guide](https://www.ssh.com/academy/ssh/hardening)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Fail2Ban Documentation](https://www.fail2ban.org/)

---

## 🎯 TL;DR - Start Here

1. **Experienced users:** → [QUICK_START.md](QUICK_START.md)
2. **Want detailed steps:** → [SECURITY_DEPLOYMENT_CHECKLIST.md](SECURITY_DEPLOYMENT_CHECKLIST.md)
3. **Setting up 2FA:** → [2fa_setup_guide.md](2fa_setup_guide.md)
4. **Got locked out:** → [emergency_recovery.md](emergency_recovery.md)
5. **Main script:** → [vps_security_hardening.sh](vps_security_hardening.sh)

**Remember:** Always create a backup before starting! 🛡️
