#!/bin/bash

# Sagatoy Frontend Deploy Script
# Deploys to Cloudflare Pages

set -e

echo "🔨 Building Next.js..."
npm run build

echo "🚀 Deploying to Cloudflare Pages..."
npx wrangler pages deploy out --project-name sagatoy --branch main

echo "✅ Deployment complete!"
echo "🌐 https://sagatoy.com"
