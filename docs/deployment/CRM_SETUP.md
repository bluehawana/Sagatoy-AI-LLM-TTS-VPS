# Sagatoy Waitlist - Dual Function CRM System

Your waitlist now has **TWO separate functions**:

## Function 1: CRM Database (Store Customer Emails)
Stores all waitlist signups in a database for email marketing campaigns when you launch.

## Function 2: Admin Notifications
Sends instant notification to info@sagatoy.com when someone joins.

---

## Setup Database for CRM (Optional but Recommended)

### Option A: Cloudflare KV (Simple)

1. Go to Cloudflare Dashboard → Workers & Pages → KV
2. Click "Create a namespace"
3. Name it: `WAITLIST_KV`
4. Go to your sagatoy Pages project → Settings → Functions → KV Namespace Bindings
5. Add binding:
   - Variable name: `WAITLIST_KV`
   - KV namespace: Select the one you created

### Option B: Cloudflare D1 (Better for SQL queries)

1. Create D1 database:
```bash
npx wrangler d1 create sagatoy-waitlist
```

2. Add to wrangler.toml:
```toml
[[d1_databases]]
binding = "WAITLIST_DB"
database_name = "sagatoy-waitlist"
database_id = "your-database-id-here"
```

3. Create table:
```sql
CREATE TABLE waitlist (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  timestamp TEXT NOT NULL,
  source TEXT,
  user_agent TEXT,
  status TEXT DEFAULT 'pending'
);
```

---

## Export Waitlist for Email Marketing

### From KV:
```bash
npx wrangler kv:key list --namespace-id=YOUR_ID
```

### From D1:
```bash
npx wrangler d1 execute sagatoy-waitlist --command="SELECT email, timestamp, source FROM waitlist ORDER BY timestamp DESC"
```

Export as CSV:
```bash
npx wrangler d1 execute sagatoy-waitlist --command="SELECT email FROM waitlist" --json > waitlist.json
```

---

## Email Marketing When You Launch (Q2 2026)

1. Export all emails from database
2. Use email marketing service (Mailchimp, SendGrid, etc.)
3. Send launch announcement to all waitlist subscribers
4. Track who becomes customers

---

## DNS Setup for Email Notifications

Add these TXT records in Cloudflare DNS:

```
Type: TXT | Name: @ | Content: v=spf1 a mx include:relay.mailchannels.net ~all
Type: TXT | Name: mailchannels._domainkey | Content: v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDPtW5iwpXVPiH5FzJ7Nrl8USzuY9zqqzjE0D1r04xDN6qwziDnmgcFNNfMewVKN2D1O+2J9N73h7mU8JAXq3o+7KLCdPiKvWBb0FJJhJLO2BhqYxLvLJQ/
Type: TXT | Name: _mailchannels | Content: v=mc1 cfid=sagatoy.pages.dev
```

---

## What Happens Now

Every waitlist signup:
1. ✅ Stores email in database (CRM)
2. ✅ Sends beautiful HTML notification to info@sagatoy.com
3. ✅ Shows success message to customer
4. ✅ Ready for email marketing when you launch!

Perfect for a real startup! 🚀
