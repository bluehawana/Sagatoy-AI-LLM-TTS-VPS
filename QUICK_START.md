# Sagatoy Quick Start Guide

## 🚀 Current Status

**Live Site**: https://sagatoy.com
**GitHub**: https://github.com/bluehawana/Sagatoy-AI-LLM-TTS-VPS

## 📋 Quick Commands

### Development
```bash
cd frontend
npm install        # First time only
npm run dev        # Start dev server (localhost:3000)
npm run build      # Build for production
```

### Deploy to Production
```bash
./deploy_to_cf.sh  # Deploy to Cloudflare Pages
```

### Git Workflow
```bash
# Start new work
git checkout dev
git pull origin dev

# Make changes
git add .
git commit -m "Your message"
git push origin dev

# Deploy to production
git checkout main
git merge dev
git push origin main
```

## 🌿 Branches

| Branch | Purpose | URL |
|--------|---------|-----|
| `main` | Production site | https://sagatoy.com |
| `dev` | Development work | Local testing |
| `feature/info-page` | Detailed info page | /info route |
| `production` | Production backup | Mirror of main |

## 📁 Project Structure

```
Sagatoy-LLM-TTS-VPS/
├── frontend/
│   ├── app/
│   │   ├── page.tsx        # Main landing page
│   │   └── info/
│   │       └── page.tsx    # Detailed info page
│   ├── public/
│   │   ├── logo.png        # Dolphin logo
│   │   └── sagatoy.jpeg    # Product image
│   ├── wrangler.toml       # Cloudflare config
│   └── package.json
├── backend/                 # FastAPI backend
├── deploy/                  # VPS deployment scripts
└── docs/                    # Documentation

```

## 🎨 Design System

### Colors
- **Primary Purple**: `#8B5CF6` (saga-purple)
- **Primary Sky**: `#38BDF8` (saga-sky)
- **Text**: `#0F172A` (saga-ink)
- **Background**: `#F8FAFC` (slate-50)

### Typography
- **Headings**: Space Grotesk (display font)
- **Body**: Inter
- **Size Scale**: text-sm → text-7xl

### Logo Sizes
- Header: 56px (h-14)
- Footer: 48px (h-12)
- Info page: 56px (h-14)

## 🔄 Common Tasks

### Update Homepage Content
```bash
git checkout dev
# Edit frontend/app/page.tsx
npm run build
git commit -am "Update homepage content"
git push origin dev
```

### Add New Feature
```bash
git checkout -b feature/new-feature dev
# Make changes
git commit -am "Add new feature"
git push origin feature/new-feature
# Create PR on GitHub
```

### Deploy New Version
```bash
git checkout main
git merge dev
cd frontend
npm run build
npx wrangler pages deploy out --project-name=sagatoy
git push origin main
```

### Rollback Production
```bash
git checkout main
git reset --hard HEAD~1  # Go back one commit
cd frontend && npm run build
npx wrangler pages deploy out --project-name=sagatoy
```

## 📦 Dependencies

### Frontend
- Next.js 14.2.35
- React 18
- TypeScript
- Tailwind CSS
- Lucide Icons

### Deployment
- Cloudflare Pages
- Wrangler CLI
- Node.js 18+

## 🔗 Useful Links

- **Live Site**: https://sagatoy.com
- **Cloudflare Dashboard**: https://dash.cloudflare.com
- **GitHub Repo**: https://github.com/bluehawana/Sagatoy-AI-LLM-TTS-VPS
- **Branching Strategy**: See `BRANCHING_STRATEGY.md`

## 💡 Tips

1. **Always work in `dev` branch** for new features
2. **Test locally** with `npm run dev` before deploying
3. **Use feature branches** for major changes
4. **Check Cloudflare Pages** dashboard for deployment status
5. **Clear browser cache** (Cmd+Shift+R) after deploying

## 🆘 Troubleshooting

### Build fails
```bash
rm -rf node_modules package-lock.json .next
npm install
npm run build
```

### Deployment fails
```bash
npx wrangler login
npx wrangler pages deploy out --project-name=sagatoy --commit-dirty=true
```

### Logo not showing
- Check file exists: `frontend/public/logo.png`
- Clear browser cache
- Verify deployment includes public folder

## 📧 Contact

**Email**: hello@sagatoy.com
**Location**: Gothenburg, Sweden 🇸🇪
