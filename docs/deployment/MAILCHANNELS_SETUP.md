# MailChannels Setup for Sagatoy Waitlist

Your waitlist form is now configured to send emails to **info@sagatoy.com** using MailChannels (free for Cloudflare).

## DNS Records Needed

Add these 3 TXT records to your sagatoy.com domain in Cloudflare DNS:

### 1. SPF Record (Authorize MailChannels)
```
Type: TXT
Name: @
Content: v=spf1 a mx include:relay.mailchannels.net ~all
```

### 2. DKIM Record (Email Authentication)
```
Type: TXT
Name: mailchannels._domainkey
Content: v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDPtW5iwpXVPiH5FzJ7Nrl8USzuY9zqqzjE0D1r04xDN6qwziDnmgcFNNfMewVKN2D1O+2J9N73h7mU8JAXq3o+7KLCdPiKvWBb0FJJhJLO2BhqYxLvLJQ/
```

### 3. Domain Lockdown (Prevent Spoofing)
```
Type: TXT
Name: _mailchannels
Content: v=mc1 cfid=sagatoy.pages.dev
```

## How to Add DNS Records

1. Go to **Cloudflare Dashboard**
2. Select your domain: **sagatoy.com**
3. Click **DNS** in the left sidebar
4. Click **Add record** for each TXT record above
5. Wait 5-10 minutes for DNS propagation

## Test Your Waitlist

Once DNS records are added:

1. Go to **www.sagatoy.com**
2. Fill in the waitlist form
3. Click "Notify Me"
4. Check **info@sagatoy.com** for the notification email!

## What Happens

Every waitlist signup sends a beautiful HTML email to info@sagatoy.com with:
- Customer's email address
- Timestamp of signup
- Source (www.sagatoy.com or info.sagatoy.com)
- Browser information

Perfect for tracking your first customers! 🚀
