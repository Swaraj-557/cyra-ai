"""
Cyra AI Assistant - Demo Script
Test the core functionality without requiring all Azure services
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.tools.password_generator import PasswordGenerator
from src.tools.tool_manager import ToolManager

async def demo_password_tools():
    """Demonstrate password generation and analysis tools"""
    print("🔐 Testing Password Generator...")
    
    password_gen = PasswordGenerator()
    
    # Generate a secure password
    print("\n1. Generating secure passwords:")
    for i in range(3):
        password = password_gen.generate_password(length=16, include_special=True)
        strength = password_gen.assess_password_strength(password)
        print(f"   Password {i+1}: {password}")
        print(f"   Strength: {strength.level} (Score: {strength.score}/100)")
        print(f"   Crack time: {strength.estimated_crack_time}")
        print()
    
    # Generate a passphrase
    print("2. Generating memorable passphrase:")
    passphrase = password_gen.generate_passphrase(word_count=4, include_numbers=True)
    passphrase_strength = password_gen.assess_password_strength(passphrase)
    print(f"   Passphrase: {passphrase}")
    print(f"   Strength: {passphrase_strength.level} (Score: {passphrase_strength.score}/100)")
    print()
    
    # Analyze weak password
    print("3. Analyzing weak password:")
    weak_password = "password123"
    weak_strength = password_gen.assess_password_strength(weak_password)
    print(f"   Password: {weak_password}")
    print(f"   Strength: {weak_strength.level} (Score: {weak_strength.score}/100)")
    print(f"   Feedback: {', '.join(weak_strength.feedback)}")
    print()
    
    # Check for breach patterns
    print("4. Checking for breach patterns:")
    test_passwords = ["qwerty123", "Password@123", "X7$mK9@nP4&vL2^qE8!"]
    for pwd in test_passwords:
        warnings = password_gen.check_breach_patterns(pwd)
        print(f"   '{pwd}': {len(warnings)} warnings")
        if warnings:
            for warning in warnings:
                print(f"     - {warning}")

async def demo_tool_manager():
    """Demonstrate tool manager functionality"""
    print("\n🛠️  Testing Tool Manager...")
    
    tool_manager = ToolManager()
    
    # Get available tools
    tools = tool_manager.get_tool_list()
    print(f"\nAvailable tools: {', '.join(tools)}")
    
    # Test password generation through tool manager
    print("\n1. Generating password through tool manager:")
    result = await tool_manager.execute_tool(
        "generate_password",
        {"length": 12, "count": 2},
        "demo_user"
    )
    
    if result["success"]:
        if "passwords" in result["result"]:
            for i, pwd_info in enumerate(result["result"]["passwords"]):
                print(f"   Password {i+1}: {pwd_info['password']} ({pwd_info['strength_level']})")
        else:
            pwd_info = result["result"]
            print(f"   Password: {pwd_info['password']}")
            print(f"   Strength: {pwd_info['strength']['level']}")
    
    # Test security advice
    print("\n2. Getting security advice:")
    advice_result = await tool_manager.execute_tool(
        "get_security_advice",
        {"topic": "password"},
        "demo_user"
    )
    
    if advice_result["success"]:
        advice = advice_result["result"]["advice"]
        print(f"   Topic: {advice_result['result']['topic']}")
        print(f"   Summary: {advice['summary']}")
        print("   Best practices:")
        for practice in advice.get("best_practices", [])[:3]:  # Show first 3
            print(f"     - {practice}")

def print_demo_header():
    """Print demo header"""
    print("""
    ░█▀▀▀█ █░░█ █▀▀█ █▀▀█ 
    ░█    █▄▄█ █▄▄▀ █▄▄█ 
    ░█▄▄▄█ ▄▄▄█ █▄▄█ █▄▄█ 
    
    🛡️  Cyra AI Assistant - Demo Mode
    🧪 Testing core functionality...
    """)

async def main():
    """Main demo function"""
    print_demo_header()
    
    try:
        await demo_password_tools()
        await demo_tool_manager()
        
        print("\n" + "="*60)
        print("✅ Demo completed successfully!")
        print("\n📋 What you've seen:")
        print("   - Secure password generation with customizable options")
        print("   - Comprehensive password strength analysis")
        print("   - Memorable passphrase creation")
        print("   - Security vulnerability pattern detection")
        print("   - Tool manager coordination system")
        print("   - Cybersecurity advice and best practices")
        
        print("\n🚀 To run the full Cyra experience:")
        print("   1. Set up your Azure OpenAI and Speech credentials in .env")
        print("   2. Run: python main.py")
        print("   3. Open http://localhost:8000 for the web interface")
        print("   4. Chat with Cyra using natural language!")
        
    except Exception as e:
        print(f"\n❌ Demo encountered an error: {e}")
        print("   This is likely due to missing dependencies or configuration.")

if __name__ == "__main__":
    asyncio.run(main())
