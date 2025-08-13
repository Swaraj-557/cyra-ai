# Git Installation Guide for Windows

## Option 1: Download Git for Windows (Recommended)

1. **Download Git:**
   - Go to: https://git-scm.com/download/win
   - Download the 64-bit Git for Windows installer
   - Run the installer with default settings

2. **After Installation:**
   - Open a new PowerShell window
   - Test: `git --version`

## Option 2: Using GitHub Desktop (Easier for beginners)

1. **Download GitHub Desktop:**
   - Go to: https://desktop.github.com/
   - Download and install GitHub Desktop
   - Sign in with your GitHub account

2. **Clone your repository:**
   - Click "Clone a repository from the Internet"
   - Enter: `https://github.com/Swaraj-557/cyra-ai.git`
   - Choose local path: `C:\Users\pc\Desktop\cyra`

## Option 3: Web-based Upload

1. **Go to your GitHub repository:**
   - Visit: https://github.com/Swaraj-557/cyra-ai
   - Click "uploading an existing file"

2. **Upload files:**
   - Drag and drop all files from `C:\Users\pc\Desktop\cyra`
   - Add commit message: "Initial commit: Cyra AI pre-launch"
   - Click "Commit changes"

## Option 4: PowerShell Commands (After Git installation)

```powershell
# Navigate to project directory
cd "C:\Users\pc\Desktop\cyra"

# Initialize repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Cyra AI pre-launch"

# Set main branch
git branch -M main

# Add remote repository
git remote add origin https://github.com/Swaraj-557/cyra-ai.git

# Push to GitHub
git push -u origin main
```

## GitHub Pages Setup (After uploading)

1. **Enable GitHub Pages:**
   - Go to your repository settings
   - Scroll to "Pages" section
   - Source: "Deploy from a branch"
   - Branch: "main"
   - Folder: "/ (root)"
   - Click "Save"

2. **Your site will be available at:**
   - `https://swaraj-557.github.io/cyra-ai/`

## Troubleshooting

- **If Git commands don't work:** Restart PowerShell after installation
- **If push fails:** Check repository permissions and authentication
- **For private repositories:** Use GitHub Desktop or personal access tokens

Choose the option that works best for you!
