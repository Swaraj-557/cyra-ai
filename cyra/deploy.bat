@echo off
REM Cyra AI - Windows Deployment Script

echo 🚀 Preparing Cyra AI for GitHub Pages deployment...

REM Check if we're in the right directory
if not exist "index.html" (
    echo ❌ Error: index.html not found. Please run this script from the project root.
    pause
    exit /b 1
)

echo ✅ Checking required files...

REM Check for required files
if exist "index.html" (echo   ✓ index.html found) else (echo   ❌ index.html missing & exit /b 1)
if exist "README.md" (echo   ✓ README.md found) else (echo   ❌ README.md missing & exit /b 1)
if exist "LICENSE" (echo   ✓ LICENSE found) else (echo   ❌ LICENSE missing & exit /b 1)
if exist "CONTRIBUTING.md" (echo   ✓ CONTRIBUTING.md found) else (echo   ❌ CONTRIBUTING.md missing & exit /b 1)
if exist "_config.yml" (echo   ✓ _config.yml found) else (echo   ❌ _config.yml missing & exit /b 1)
if exist "package.json" (echo   ✓ package.json found) else (echo   ❌ package.json missing & exit /b 1)

REM Check GitHub Actions workflow
if exist ".github\workflows\deploy.yml" (
    echo   ✓ GitHub Actions workflow found
) else (
    echo   ❌ GitHub Actions workflow missing
    exit /b 1
)

echo.
echo 🎉 Cyra AI is ready for GitHub Pages deployment!
echo.
echo 📋 Next steps:
echo 1. Create a new repository on GitHub
echo 2. Push this code to the repository:
echo    git init
echo    git add .
echo    git commit -m "Initial commit: Cyra AI pre-launch"
echo    git branch -M main
echo    git remote add origin https://github.com/YOUR-USERNAME/cyra-ai.git
echo    git push -u origin main
echo.
echo 3. Enable GitHub Pages in repository settings:
echo    - Go to Settings → Pages
echo    - Source: Deploy from a branch
echo    - Branch: main / (root)
echo.
echo 4. Your site will be available at:
echo    https://YOUR-USERNAME.github.io/cyra-ai/
echo.
echo 🌐 Don't forget to update the URLs in:
echo    - README.md
echo    - _config.yml
echo    - package.json
echo.
echo ✨ Happy deploying!
echo.
pause
