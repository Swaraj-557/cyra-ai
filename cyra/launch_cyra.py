"""
Cyra AI Assistant Launcher
Checks configuration and starts the web application
"""
import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_environment():
    """Check if environment is properly configured"""
    print("🔧 Checking environment configuration...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("   Please copy .env.example to .env and configure your Azure credentials")
        return False
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_DEPLOYMENT_NAME"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            return False
        
        print("✅ Environment configuration looks good")
        return True
        
    except Exception as e:
        print(f"❌ Error checking environment: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"), 
        ("openai", "openai"),
        ("python-dotenv", "dotenv"),
        ("pydantic-settings", "pydantic_settings")
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("   Please install them with: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All required dependencies are installed")
    return True

async def test_core_functionality():
    """Test core functionality without external services"""
    print("🧪 Testing core functionality...")
    
    try:
        from src.tools.password_generator import PasswordGenerator
        from src.tools.tool_manager import ToolManager
        
        # Test password generator
        pg = PasswordGenerator()
        password = pg.generate_password(length=12)
        strength = pg.assess_password_strength(password)
        
        # Test tool manager
        tm = ToolManager()
        tools = tm.get_tool_list()
        
        print(f"✅ Core functionality working (Generated password: {password[:4]}...)")
        print(f"   Available tools: {len(tools)} tools ready")
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False

def start_web_server():
    """Start the Cyra web application"""
    print("🚀 Starting Cyra web application...")
    
    try:
        import uvicorn
        from src.core.config import get_settings
        
        settings = get_settings()
        
        print(f"🌐 Starting server at http://{settings.host}:{settings.port}")
        print("📖 API documentation will be available at: http://localhost:8000/docs")
        print("💬 Chat interface will be available at: http://localhost:8000")
        print("\n🛡️ Cyra AI Assistant is ready to help with cybersecurity!")
        
        uvicorn.run(
            "src.core.app:app",
            host=settings.host,
            port=settings.port,
            reload=settings.debug,
            log_level=settings.log_level.lower()
        )
        
    except Exception as e:
        print(f"❌ Failed to start web server: {e}")
        return False

async def main():
    """Main launcher function"""
    print("""
    ░█▀▀▀█ █░░█ █▀▀█ █▀▀█ 
    ░█    █▄▄█ █▄▄▀ █▄▄█ 
    ░█▄▄▄█ ▄▄▄█ █▄▄█ █▄▄█ 
    
    🛡️  Cyra AI Assistant Launcher
    🚀 Preparing your cybersecurity companion...
    """)
    
    # Run all checks
    checks = [
        check_environment(),
        check_dependencies(),
        await test_core_functionality()
    ]
    
    if all(checks):
        print("\n" + "="*50)
        print("✅ All checks passed! Starting Cyra...")
        start_web_server()
    else:
        print("\n❌ Some checks failed. Please fix the issues above before starting Cyra.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
