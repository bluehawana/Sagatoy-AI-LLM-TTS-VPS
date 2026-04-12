# Deployment Scripts

Scripts for deploying and configuring the VPS.

## Files

- `sagatoy.service` - Systemd service file
- `nginx_config_sagatoy.conf` - Nginx configuration
- `deploy_sagatoy.sh` - Main deployment script
- `vps_setup_sagatoy.sh` - VPS initial setup
- `secure_vps.sh` - Security hardening
- `vps_security_hardening.sh` - Additional hardening
- `ssl_setup.sh` - SSL certificate setup
- `ssl_setup_quick.sh` - Quick SSL setup
- `secure_ssl_setup.sh` - Secure SSL setup
- `ultra_secure_setup.sh` - Maximum security setup

## 2FA Scripts

- `complete_2fa_setup.sh` - Complete 2FA setup
- `fix_2fa_correct.sh` - Fix 2FA issues
- `fix_2fa_now.sh` - Quick 2FA fix
- `diagnose_2fa.sh` - Diagnose 2FA problems
- `check_ssh_config.sh` - Check SSH configuration

## Usage

```bash
# Copy service file to VPS
scp -P 1025 deploy/sagatoy.service harvard@your-vps:/etc/systemd/system/

# Copy nginx config
scp -P 1025 deploy/nginx_config_sagatoy.conf harvard@your-vps:/etc/nginx/sites-available/
```
