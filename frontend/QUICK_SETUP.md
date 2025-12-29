# Quick Setup - 2 Minutes ⚡

## ✅ Step 1: Add DNS Records (Email Notifications)

Go to: **Cloudflare Dashboard** → **sagatoy.com** → **DNS** → **Records**

Click "Add record" for each:

### Record 1: SPF
```
Type: TXT
Name: @
Content: v=spf1 a mx include:relay.mailchannels.net ~all
TTL: Auto
```

### Record 2: DKIM
```
Type: TXT
Name: mailchannels._domainkey
Content: v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDPtW5iwpXVPiH5FzJ7Nrl8USzuY9zqqzjE0D1r04xDN6qwziDnmgcFNNfMewVKN2D1O+2J9N73h7mU8JAXq3o+7KLCdPiKvWBb0FJJhJLO2BhqYxLvLJQ/
TTL: Auto
```

### Record 3: Domain Lock
```
Type: TXT
Name: _mailchannels
Content: v=mc1 cfid=sagatoy.pages.dev
TTL: Auto
```

---

## ✅ Step 2: Bind KV Database (CRM Storage)

**KV Namespace Created**: `WAITLIST_KV`
**ID**: `fed53664b2c041cd9caf42c60f7d7e6e`

Go to: **Cloudflare Dashboard** → **Workers & Pages** → **sagatoy** → **Settings** → **Functions** → **KV namespace bindings**

Click "Add binding":
```
Variable name: WAITLIST_KV
KV namespace: WAITLIST_KV (fed53664b2c041cd9caf42c60f7d7e6e)
Environment: Production
```

Click "Save"

---

## ✅ Step 3: Test It!

1. Go to **www.sagatoy.com**
2. Scroll to waitlist form
3. Enter your email
4. Click "Notify Me"
5. Check **info@sagatoy.com** for the notification email!

---

## 📊 View Your Waitlist

**Cloudflare Dashboard** → **Workers & Pages** → **KV** → **WAITLIST_KV** → View all entries

Every signup is stored with:
- Email address
- Timestamp
- Source (www or info site)
- Browser info
- Status

---

## 🚀 Export for Email Marketing

When ready to launch (Q2 2026):

```bash
npx wrangler kv key list --namespace-id=fed53664b2c041cd9caf42c60f7d7e6e
```

Use these emails for your launch marketing campaign!

---

**That's it! Your startup waitlist is ready!** 🎉
