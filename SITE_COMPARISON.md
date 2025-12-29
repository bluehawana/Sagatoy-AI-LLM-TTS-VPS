# Sagatoy Website Comparison

## 🌐 Live Sites Overview

### **Main Site** - https://sagatoy.com
**Branch**: `main`
**Purpose**: Professional conversion-focused landing page
**Audience**: External visitors, potential customers

**Design Features**:
- ✅ Clean, minimal Vercel-style design
- ✅ Logo + brand name in header (dolphin PNG 213KB)
- ✅ Professional navigation menu
- ✅ Concise hero section with large typography (up to 7xl)
- ✅ Single email signup form
- ✅ 3 feature cards with clean borders
- ✅ 3-column professional footer
- ✅ Optimized for conversion and quick load times

**Tech**:
- Next.js static export
- Cloudflare Pages
- Custom domain: sagatoy.com

---

### **Info Site** - https://info.sagatoy.com
**Branch**: `feature/info-page`
**Purpose**: Detailed product information page
**Audience**: Interested users wanting more details

**Design Features**:
- ✅ Original coming soon design with glass effects
- ✅ Large logo.svg with full branding (2.3MB)
- ✅ Animated gradient backgrounds with blur effects
- ✅ Glass morphism design elements
- ✅ Detailed product description
- ✅ Prominent status badge with pulse animation
- ✅ Floating "5 Languages" badge on product image
- ✅ "What to Expect" section with larger feature cards
- ✅ More visual elements and comprehensive content

**Tech**:
- Next.js static export
- Cloudflare Pages (separate project: sagatoy-info)
- Custom subdomain: info.sagatoy.com

---

## 📊 Side-by-Side Comparison

| Feature | sagatoy.com | info.sagatoy.com |
|---------|-------------|------------------|
| **Design Style** | Professional, minimal | Visual, detailed |
| **Logo** | Dolphin PNG (213KB) | Logo SVG with text (2.3MB) |
| **Header** | Logo + brand + nav | Logo only |
| **Hero Title** | 5-7xl responsive | 5-6xl |
| **Background** | Subtle gradients | Animated blurred orbs |
| **Email Form** | Rounded-xl modern | Rounded-full classic |
| **CTA Button** | Dark (saga-ink) | Gradient (purple→sky) |
| **Status Badge** | Small, clean | Large with glass effect |
| **Feature Cards** | Clean borders, hover | Glass effect, centered |
| **Footer** | 3-column detailed | Centered, simple |
| **Page Size** | ~101KB JS | ~101KB JS (same) |
| **Load Time** | Very fast | Very fast |
| **Conversion Focus** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Information Depth** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 Use Cases

### Use **sagatoy.com** for:
- 🎯 Social media links
- 📧 Email campaigns
- 💼 Investor presentations
- 📱 First impressions
- 🔄 Quick conversions

### Use **info.sagatoy.com** for:
- 📚 Detailed product information
- 🤔 Users who want to learn more
- 📖 Press and media inquiries
- 👥 Partner/investor deep dives
- 🔗 "Learn More" button destination

---

## 🔄 Update Workflow

### Update Main Site (sagatoy.com)
```bash
git checkout main
# Edit frontend/app/page.tsx
cd frontend
npm run build
npx wrangler pages deploy out --project-name=sagatoy
git commit -am "Update main site"
git push origin main
```

### Update Info Site (info.sagatoy.com)
```bash
git checkout feature/info-page
# Edit frontend/app/page.tsx
cd frontend
npm run build
npx wrangler pages deploy out --project-name=sagatoy-info
git commit -am "Update info site"
git push origin feature/info-page
```

---

## 📈 Analytics Tracking

Both sites share the same structure, making it easy to compare:

**Main Site Metrics**:
- Bounce rate
- Email signup conversion
- Time on page
- Click-through rate

**Info Site Metrics**:
- Engagement time
- Scroll depth
- Content consumption
- Detail interest level

---

## 🎨 Design Systems

### Shared Elements
- **Colors**: saga-purple (#8B5CF6), saga-sky (#38BDF8)
- **Typography**: Space Grotesk (headings), Inter (body)
- **Components**: Both use same Lucide icons
- **Framework**: Same Next.js 14 build

### Differences
- **Layout**: Main (12-col grid) vs Info (2-col)
- **Effects**: Main (subtle) vs Info (pronounced)
- **Spacing**: Main (tighter) vs Info (more generous)

---

## 🚀 Deployment Status

| Site | URL | Status | Last Updated |
|------|-----|--------|--------------|
| Main | sagatoy.com | ✅ Live | Dec 29, 2025 |
| Main (CF) | sagatoy.pages.dev | ✅ Live | Dec 29, 2025 |
| Info | info.sagatoy.com | ✅ Live | Dec 29, 2025 |
| Info (CF) | sagatoy-info.pages.dev | ✅ Live | Dec 29, 2025 |

---

## 📝 Content Strategy

**Main Site** (sagatoy.com):
> "AI Companion For Your Child"
- Brief, punchy copy
- Clear value proposition
- Single CTA (email signup)
- Professional trust signals

**Info Site** (info.sagatoy.com):
> "AI Companion For Your Child"
- Same headline, more context
- Detailed feature explanations
- Visual storytelling
- Educational approach

---

## 🔗 Cross-Linking Strategy

Consider adding to main site:
```tsx
<Link href="https://info.sagatoy.com">Learn More →</Link>
```

Consider adding to info site:
```tsx
<Link href="https://sagatoy.com">← Back to Home</Link>
```

---

## 📞 Contact

**Main Site**: hello@sagatoy.com
**Info Site**: hello@sagatoy.com (same)
**Location**: Gothenburg, Sweden 🇸🇪

---

*Last updated: December 29, 2025*
