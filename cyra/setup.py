#!/usr/bin/env python3
"""
Setup script for Cyra AI Assistant
This script helps set up the development environment and initial configuration.
"""
import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    print("""
    ░█▀▀▀█ █░░█ █▀▀█ █▀▀█ 
    ░█    █▄▄█ █▄▄▀ █▄▄█ 
    ░█▄▄▄█ ▄▄▄█ █▄▄█ █▄▄█ 
    
    🛡️  Cyra AI Assistant Setup
    🚀 Setting up your cybersecurity companion...
    """)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version {sys.version.split()[0]} is compatible")

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("   Please run: pip install -r requirements.txt")
        return False
    return True

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ .env.example file not found")
        return False
    
    # Copy .env.example to .env
    with open(env_example, 'r') as source:
        content = source.read()
    
    with open(env_file, 'w') as target:
        target.write(content)
    
    print("📝 Created .env file from template")
    print("⚠️  Please edit .env file with your Azure credentials:")
    print("   - AZURE_OPENAI_ENDPOINT")
    print("   - AZURE_OPENAI_API_KEY") 
    print("   - AZURE_OPENAI_DEPLOYMENT_NAME")
    print("   - AZURE_SPEECH_KEY")
    print("   - AZURE_SPEECH_REGION")
    print("   - SECRET_KEY (generate a secure random string)")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "data", "temp"]
    
    for dir_name in directories:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"📁 Created directory: {dir_name}")
        else:
            print(f"✅ Directory exists: {dir_name}")

def run_tests():
    """Run basic tests to verify setup"""
    print("🧪 Running basic tests...")
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/test_password_generator.py", "-v"], 
                               capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Basic tests passed")
            return True
        else:
            print("⚠️  Some tests failed, but setup can continue")
            print(result.stdout)
            print(result.stderr)
            return True
    except subprocess.TimeoutExpired:
        print("⚠️  Tests timed out, but setup can continue")
        return True
    except Exception as e:
        print(f"⚠️  Could not run tests: {e}")
        return True

def check_azure_config():
    """Check if Azure configuration looks valid"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_KEY", 
            "AZURE_OPENAI_DEPLOYMENT_NAME",
            "AZURE_SPEECH_KEY",
            "AZURE_SPEECH_REGION"
        ]
        
        missing_vars = []
        for var in required_vars:
            value = os.getenv(var)
            if not value or value.startswith("your_"):
                missing_vars.append(var)
        
        if missing_vars:
            print("⚠️  Azure configuration incomplete:")
            for var in missing_vars:
                print(f"   - {var}")
            print("   Please update your .env file with valid Azure credentials")
            return False
        else:
            print("✅ Azure configuration appears complete")
            return True
            
    except ImportError:
        print("⚠️  Could not check Azure config (python-dotenv not installed)")
        return True

def main():
    """Main setup function"""
    print_banner()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success = True
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    if not install_requirements():
        success = False
    
    # Create .env file
    if not create_env_file():
        success = False
    
    # Create directories
    create_directories()
    
    # Check Azure configuration
    check_azure_config()
    
    # Run tests
    run_tests()
    
    print("\n" + "="*50)
    if success:
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit .env file with your Azure credentials")
        print("2. Run: python main.py")
        print("3. Open http://localhost:8000 in your browser")
        print("4. Start chatting with Cyra!")
    else:
        print("⚠️  Setup completed with some issues")
        print("   Please resolve the issues above and try again")
    
    print("\n🔗 Useful links:")
    print("   - Azure OpenAI: https://azure.microsoft.com/en-us/products/ai-services/openai-service")
    print("   - Azure Speech: https://azure.microsoft.com/en-us/products/ai-services/speech-to-text")
    print("   - Documentation: README.md")

if __name__ == "__main__":
    main()
