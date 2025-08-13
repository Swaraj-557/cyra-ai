"""
Quick test of Cyra with GPT-4.1 configuration
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_cyra_config():
    """Test if Cyra can connect to Azure OpenAI with gpt-4.1"""
    try:
        from src.core.config import get_settings
        from src.core.ai_brain import AIBrain
        
        print("🔧 Testing Cyra configuration...")
        
        # Check settings
        settings = get_settings()
        print(f"✅ Settings loaded successfully")
        print(f"   Deployment: {settings.azure_openai_deployment_name}")
        print(f"   Endpoint: {settings.azure_openai_endpoint}")
        
        # Test AI Brain
        print("\n🤖 Testing AI Brain connection...")
        ai_brain = AIBrain()
        
        # Simple test message
        result = await ai_brain.process_message(
            "Hello, can you introduce yourself briefly?", 
            "test_user"
        )
        
        print("✅ AI Brain connected successfully!")
        print(f"   Response: {result['response'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_password_tools():
    """Test password generation tools"""
    try:
        from src.tools.password_generator import PasswordGenerator
        
        print("\n🔐 Testing Password Tools...")
        pg = PasswordGenerator()
        
        # Generate password
        password = pg.generate_password(length=16)
        strength = pg.assess_password_strength(password)
        
        print(f"✅ Generated password: {password}")
        print(f"   Strength: {strength.level} ({strength.score}/100)")
        
        return True
        
    except Exception as e:
        print(f"❌ Password tools test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("""
    ░█▀▀▀█ █░░█ █▀▀█ █▀▀█ 
    ░█    █▄▄█ █▄▄▀ █▄▄█ 
    ░█▄▄▄█ ▄▄▄█ █▄▄█ █▄▄█ 
    
    🛡️  Cyra Configuration Test
    🧪 Testing GPT-4.1 setup...
    """)
    
    # Test password tools (no API required)
    tools_ok = await test_password_tools()
    
    # Test AI configuration (requires API)
    config_ok = await test_cyra_config()
    
    print("\n" + "="*50)
    if tools_ok and config_ok:
        print("🎉 All tests passed! Cyra is ready to go!")
        print("\n🚀 To start Cyra:")
        print("   python main.py")
        print("   Then visit: http://localhost:8000")
    elif tools_ok:
        print("⚠️  Password tools work, but check your Azure OpenAI configuration")
        print("   Verify your deployment name 'gpt-4.1' exists in Azure")
    else:
        print("❌ Tests failed. Check your configuration.")

if __name__ == "__main__":
    asyncio.run(main())
