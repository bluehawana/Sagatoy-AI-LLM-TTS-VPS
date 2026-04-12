# Manual SSL Setup Guide for sagatoy.com

## Prerequisites
- DNS already configured: sagatoy.com and www.sagatoy.com → 94.72.141.71 ✓
- VPS: Ubuntu 22.04 at 94.72.141.71

## Step 1: Connect to VPS
```bash
ssh harvad@94.72.141.71
```

## Step 2: Update System
```bash
sudo apt update && sudo apt upgrade -y
```

## Step 3: Install Required Packages
```bash
sudo apt install -y nginx certbot python3-certbot-nginx ufw fail2ban
```

## Step 4: Configure Firewall
```bash
# Enable UFW firewall
sudo ufw --force enable

# Allow SSH (IMPORTANT: Do this first!)
sudo ufw allow OpenSSH

# Allow HTTP and HTTPS
sudo ufw allow 'Nginx Full'

# Check status
sudo ufw status
```

## Step 5: Stop Apache (if running)
```bash
sudo systemctl stop apache2 2>/dev/null || true
sudo systemctl disable apache2 2>/dev/null || true
```

## Step 6: Create Website Directory
```bash
sudo mkdir -p /var/www/sagatoy.com
sudo chown -R www-data:www-data /var/www/sagatoy.com
sudo chmod -R 755 /var/www/sagatoy.com
```

## Step 7: Create Test Homepage
```bash
sudo tee /var/www/sagatoy.com/index.html > /dev/null <<'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to SagaToy</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        h1 { font-size: 3em; margin-bottom: 20px; }
        p { font-size: 1.2em; }
        .secure { color: #4ade80; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🎮 Welcome to SagaToy.com</h1>
    <p class="secure">✓ Your secure website is now online with SSL!</p>
    <p>Powered by Nginx + Let's Encrypt</p>
</body>
</html>
EOF
```

## Step 8: Configure Nginx
```bash
sudo tee /etc/nginx/sites-available/sagatoy.com > /dev/null <<'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name sagatoy.com www.sagatoy.com;

    root /var/www/sagatoy.com;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF
```

## Step 9: Enable Site
```bash
# Enable the site
sudo ln -sf /etc/nginx/sites-available/sagatoy.com /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# If test passes, restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## Step 10: Obtain SSL Certificate
```bash
# This will automatically configure HTTPS and redirect HTTP to HTTPS
sudo certbot --nginx -d sagatoy.com -d www.sagatoy.com --non-interactive --agree-tos --email admin@sagatoy.com --redirect
```

## Step 11: Set Up Auto-Renewal
```bash
# Enable and start the certbot timer
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Test renewal process
sudo certbot renew --dry-run
```

## Step 12: Configure Fail2Ban (Security)
```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Step 13: Verify SSL is Working
```bash
# Check certificate info
sudo certbot certificates

# Check Nginx status
sudo systemctl status nginx

# Test from command line
curl -I https://sagatoy.com
```

## Step 14: Configure Cloudflare SSL/TLS Settings

1. Log into Cloudflare dashboard
2. Go to SSL/TLS settings for sagatoy.com
3. Set SSL/TLS encryption mode to **"Full (strict)"**
4. Enable these settings:
   - Always Use HTTPS: ON
   - Automatic HTTPS Rewrites: ON
   - Minimum TLS Version: TLS 1.2
5. Go to SSL/TLS → Edge Certificates:
   - Enable "Always Use HTTPS"
   - Enable "HSTS" (HTTP Strict Transport Security)
6. Now you can enable Cloudflare proxy (orange cloud) on your DNS records

## Step 15: Change Default Password (IMPORTANT!)
```bash
# Change the password from default
passwd

# Follow prompts to set a strong password
```

## Verification Checklist
- [ ] Visit http://sagatoy.com (should redirect to HTTPS)
- [ ] Visit https://sagatoy.com (should show secure padlock)
- [ ] Visit https://www.sagatoy.com (should work)
- [ ] Check SSL rating at: https://www.ssllabs.com/ssltest/analyze.html?d=sagatoy.com
- [ ] Verify auto-renewal: `sudo certbot renew --dry-run`

## Troubleshooting

### If Certbot fails:
```bash
# Check if port 80/443 are accessible
sudo netstat -tlnp | grep -E ':(80|443)'

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Manually verify DNS
nslookup sagatoy.com
```

### If website doesn't load:
```bash
# Check Nginx status
sudo systemctl status nginx

# Check firewall
sudo ufw status

# View Nginx error logs
sudo tail -30 /var/log/nginx/error.log
```

## SSL Certificate Renewal
Certificates auto-renew via cron. To manually renew:
```bash
sudo certbot renew
sudo systemctl reload nginx
```

## Next Steps
1. Upload your actual website content to `/var/www/sagatoy.com/`
2. Set up SSH key authentication
3. Configure regular backups
4. Monitor SSL certificate expiration
5. Consider setting up a staging environment

## Security Best Practices Applied
✓ Firewall (UFW) enabled
✓ Fail2ban installed for brute-force protection
✓ SSL/TLS encryption with Let's Encrypt
✓ Auto-renewal configured
✓ Security headers in Nginx
✓ HTTPS redirect enforced
