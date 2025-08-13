"""
Cyra Professional - Quick Fix Script
===================================
"""
import os
import subprocess
import sys

def install_packages():
    """Install required packages"""
    print("📦 Installing packages...")
    packages = [
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0", 
        "websockets>=12.0",
        "openai>=1.3.0",
        "python-dotenv>=1.0.0"
    ]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"✅ Installed {package}")
        except:
            print(f"❌ Failed to install {package}")

def create_directories():
    """Create required directories"""
    print("📁 Creating directories...")
    dirs = ["assets", "assets/icons", "logs", "src/ui"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✅ Created {d}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        print("📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("""# Cyra Configuration
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your_endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-01
HOST=127.0.0.1
PORT=8005
""")
        print("✅ .env file created")

def start_cyra():
    """Start Cyra Professional"""
    print("🚀 Starting Cyra Professional...")
    try:
        subprocess.run(["taskkill", "/f", "/im", "python.exe"], capture_output=True)
    except:
        pass
    
    try:
        subprocess.run([sys.executable, "cyra_professional.py"])
    except KeyboardInterrupt:
        print("\\n🛑 Stopped by user")

def main():
    print("🔧 Cyra Professional Quick Fix")
    print("=" * 30)
    
    install_packages()
    create_directories() 
    create_env_file()
    
    print("\\n✅ Setup complete!")
    print("📍 Next: Configure your API keys in .env file")
    print("🚀 Then run: python cyra_professional.py")

if __name__ == "__main__":
    main()
