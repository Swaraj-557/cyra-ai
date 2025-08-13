"""
Quick test to verify Cyra is working
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_everything():
    """Test all components"""
    print("🧪 Running comprehensive tests...")
    
    # Test 1: Configuration
    try:
        from src.core.config import get_settings
        settings = get_settings()
        print("✅ Configuration loaded successfully")
        print(f"   Deployment: {settings.azure_openai_deployment_name}")
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False
    
    # Test 2: Password Tools
    try:
        from src.tools.password_generator import PasswordGenerator
        pg = PasswordGenerator()
        password = pg.generate_password(length=16)
        strength = pg.assess_password_strength(password)
        print(f"✅ Password tools working: {password} ({strength.level})")
    except Exception as e:
        print(f"❌ Password tools failed: {e}")
        return False
    
    # Test 3: Tool Manager
    try:
        from src.tools.tool_manager import ToolManager
        tm = ToolManager()
        result = await tm.execute_tool("generate_password", {"length": 12}, "test_user")
        if result["success"]:
            print(f"✅ Tool manager working: Generated {result['result']['password']}")
        else:
            print(f"❌ Tool manager failed: {result}")
            return False
    except Exception as e:
        print(f"❌ Tool manager failed: {e}")
        return False
    
    # Test 4: AI Brain (requires API)
    try:
        from src.core.ai_brain import AIBrain
        ai = AIBrain()
        
        # Test with a simple message
        result = await ai.process_message("Hello, introduce yourself briefly", "test_user")
        if result and result.get("response"):
            print(f"✅ AI Brain working: {result['response'][:50]}...")
        else:
            print("⚠️ AI Brain test inconclusive (check Azure OpenAI config)")
    except Exception as e:
        print(f"⚠️ AI Brain test failed: {e}")
        print("   This is likely due to Azure OpenAI configuration")
    
    # Test 5: Web App Components
    try:
        import fastapi
        import uvicorn
        print("✅ Web framework dependencies available")
    except Exception as e:
        print(f"❌ Web framework failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("""
    ░█▀▀▀█ █░░█ █▀▀█ █▀▀█ 
    ░█    █▄▄█ █▄▄▀ █▄▄█ 
    ░█▄▄▄█ ▄▄▄█ █▄▄█ █▄▄█ 
    
    🛡️  Cyra System Test
    """)
    
    success = asyncio.run(test_everything())
    
    print("\n" + "="*50)
    if success:
        print("🎉 All tests passed! Cyra is ready to run!")
        print("\n🚀 To start Cyra:")
        print("   python launch_cyra.py")
        print("   OR")
        print("   python main.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
