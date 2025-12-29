# Git Branching Strategy

## Overview

This repository uses a multi-branch strategy to manage different versions and environments of the Sagatoy landing page.

## Branch Structure

### 🚀 `main` (Production)
- **Purpose**: Production-ready code deployed to https://sagatoy.com
- **Deploys to**: Cloudflare Pages (sagatoy.pages.dev)
- **Protection**: Protected branch, requires review before merge
- **Description**: Clean, professional Vercel-style landing page

**Current Features:**
- Professional navigation with logo + brand name
- Hero section with email waitlist
- Feature cards (Voice, Languages, Privacy)
- 3-column footer with contact info
- Optimized for conversion

### 🏭 `production`
- **Purpose**: Stable production mirror
- **Same as**: `main` branch
- **Use case**: Backup and rollback point

### 🔧 `dev` (Development)
- **Purpose**: Active development branch
- **Use case**: Day-to-day development work
- **Testing**: Local development and testing
- **Merge to**: `main` after testing

**Workflow:**
```bash
git checkout dev
# Make changes
git add .
git commit -m "Add feature XYZ"
git push origin dev

# When ready for production
git checkout main
git merge dev
git push origin main
```

### 📄 `feature/info-page`
- **Purpose**: Detailed information page
- **Route**: `/info` or separate deployment
- **Description**: Original full-information landing page with more content

**Features:**
- Detailed product information
- Larger hero section with glass effects
- Prominent call-to-action
- More visual elements
- Better for in-depth product exploration

## Deployment Workflows

### Production Deployment (main)
```bash
cd frontend
npm run build
npx wrangler pages deploy out --project-name=sagatoy --branch=main
```

### Development Testing (dev)
```bash
cd frontend
npm run dev
# Test at http://localhost:3000
```

### Info Page Deployment
```bash
git checkout feature/info-page
cd frontend
npm run build
npx wrangler pages deploy out --project-name=sagatoy-info --branch=info
```

## Use Cases

### 1. **Quick Marketing Updates** → Use `main`
Professional, conversion-optimized page for external visitors

### 2. **Detailed Product Info** → Use `feature/info-page`
Comprehensive information for interested users

### 3. **Experimentation** → Use `dev`
Test new features, designs, or content

## Cloudflare Pages Configuration

### Main Site
- **Project**: sagatoy
- **Production branch**: main
- **URL**: https://sagatoy.pages.dev
- **Custom domain**: https://sagatoy.com

### Info Page (Optional)
- **Project**: sagatoy-info
- **Production branch**: feature/info-page
- **URL**: https://sagatoy-info.pages.dev
- **Custom domain**: https://info.sagatoy.com (optional)

## Best Practices

1. **Always work in `dev`** for new features
2. **Test locally** before merging to `main`
3. **Create feature branches** for major changes:
   ```bash
   git checkout -b feature/email-integration dev
   ```
4. **Keep branches in sync**:
   ```bash
   git checkout dev
   git pull origin main  # Stay updated with production
   ```

5. **Clean up merged branches**:
   ```bash
   git branch -d feature/completed-feature
   ```

## Example Workflows

### Scenario 1: Update CTA Button
```bash
git checkout dev
# Edit frontend/app/page.tsx
git add frontend/app/page.tsx
git commit -m "Update CTA button text and styling"
git push origin dev

# Test deployment
cd frontend && npm run build

# Merge to production
git checkout main
git merge dev
git push origin main
```

### Scenario 2: Create New Landing Page Variant
```bash
git checkout -b feature/enterprise-page dev
# Create new enterprise-focused landing page
git add .
git commit -m "Add enterprise landing page"
git push origin feature/enterprise-page

# Deploy to preview
cd frontend
npx wrangler pages deploy out --branch=enterprise
```

### Scenario 3: Hotfix in Production
```bash
git checkout -b hotfix/typo-fix main
# Fix typo
git commit -am "Fix typo in hero section"
git push origin hotfix/typo-fix

# Merge to main
git checkout main
git merge hotfix/typo-fix
git push origin main

# Backport to dev
git checkout dev
git merge hotfix/typo-fix
git push origin dev
```

## Branch Comparison

| Feature | main | dev | feature/info-page |
|---------|------|-----|-------------------|
| Style | Professional, minimal | Same as main | Detailed, visual |
| Content | Brief, focused | Experimental | Comprehensive |
| Audience | External visitors | Internal testing | Interested users |
| CTA | Email signup | Testing | Multiple CTAs |
| Deploy | Auto (CF Pages) | Manual testing | Optional deploy |

## Questions?

Contact: hello@sagatoy.com
