#!/bin/bash

# Cyra AI - GitHub Pages Deployment Script
echo "🚀 Preparing Cyra AI for GitHub Pages deployment..."

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found. Please run this script from the project root."
    exit 1
fi

# Validate HTML
echo "✅ Validating HTML..."
if command -v html5validator &> /dev/null; then
    html5validator --root . --also-check-css
    echo "✅ HTML validation complete"
else
    echo "⚠️  HTML validator not found. Install with: pip install html5validator"
fi

# Check for required files
echo "✅ Checking required files..."
required_files=("index.html" "README.md" "LICENSE" "CONTRIBUTING.md" "_config.yml" "package.json")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file found"
    else
        echo "  ❌ $file missing"
        exit 1
    fi
done

# Check GitHub Actions workflow
if [ -f ".github/workflows/deploy.yml" ]; then
    echo "  ✓ GitHub Actions workflow found"
else
    echo "  ❌ GitHub Actions workflow missing"
    exit 1
fi

echo ""
echo "🎉 Cyra AI is ready for GitHub Pages deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Push this code to the repository:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit: Cyra AI pre-launch'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/YOUR-USERNAME/cyra-ai.git"
echo "   git push -u origin main"
echo ""
echo "3. Enable GitHub Pages in repository settings:"
echo "   - Go to Settings → Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main / (root)"
echo ""
echo "4. Your site will be available at:"
echo "   https://YOUR-USERNAME.github.io/cyra-ai/"
echo ""
echo "🌐 Don't forget to update the URLs in:"
echo "   - README.md"
echo "   - _config.yml"
echo "   - package.json"
echo ""
echo "✨ Happy deploying!"
