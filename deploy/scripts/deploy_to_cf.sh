#!/bin/bash

# Deploy Sagatoy to Cloudflare Pages

set -e

echo "🚀 Deploying Sagatoy to Cloudflare Pages..."
echo ""

cd "$(dirname "$0")/frontend"

# Build
echo "📦 Building Next.js..."
npm run build

echo ""
echo "☁️  Deploying to Cloudflare Pages..."
echo ""

# Deploy using Wrangler Pages
npx wrangler pages deploy .next --project-name=sagatoy --branch=main

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌍 Your site will be live at:"
echo "   👉 https://sagatoy.pages.dev"
echo "   👉 Configure custom domain (sagatoy.com) in Cloudflare dashboard"
echo ""
