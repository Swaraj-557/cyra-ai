"""
Test Cyra's New Friendly & Short Response Mode
==============================================

This script demonstrates the improvements made to Cyra:
1. Shorter, friendlier responses
2. Call mode optimization
3. Better conversational flow
"""
import asyncio
import aiohttp
import json

async def test_normal_chat():
    """Test normal chat mode (should be friendly but can be longer)"""
    print("🗣️  Testing Normal Chat Mode:")
    print("=" * 40)
    
    async with aiohttp.ClientSession() as session:
        # Test normal password request
        message = {
            "message": "Hey Cyra, can you generate a secure password for me?",
            "user_id": "test_user",
            "is_voice_call": False
        }
        
        async with session.post('http://localhost:8004/chat', 
                                json=message) as response:
            data = await response.json()
            print(f"User: {message['message']}")
            print(f"Cyra: {data['response']}")
            print(f"Response length: {len(data['response'])} characters")
            print()

async def test_voice_call_mode():
    """Test voice call mode (should be extra short and conversational)"""
    print("📞 Testing Voice Call Mode:")
    print("=" * 40)
    
    async with aiohttp.ClientSession() as session:
        # Test voice call password request
        message = {
            "message": "Generate a password",
            "user_id": "test_user", 
            "is_voice_call": True
        }
        
        async with session.post('http://localhost:8004/chat',
                                json=message) as response:
            data = await response.json()
            print(f"User: {message['message']}")
            print(f"Cyra: {data['response']}")
            print(f"Response length: {len(data['response'])} characters")
            print()
            
        # Test casual conversation in call mode
        message2 = {
            "message": "How's it going?",
            "user_id": "test_user",
            "is_voice_call": True
        }
        
        async with session.post('http://localhost:8004/chat',
                                json=message2) as response:
            data = await response.json()
            print(f"User: {message2['message']}")
            print(f"Cyra: {data['response']}")
            print(f"Response length: {len(data['response'])} characters")
            print()

async def test_comparison():
    """Compare the same question in both modes"""
    print("🔄 Comparison Test - Same Question, Both Modes:")
    print("=" * 50)
    
    question = "What's the best way to stay safe online?"
    
    async with aiohttp.ClientSession() as session:
        # Normal mode
        normal_msg = {
            "message": question,
            "user_id": "test_user",
            "is_voice_call": False
        }
        
        async with session.post('http://localhost:8004/chat',
                                json=normal_msg) as response:
            normal_data = await response.json()
        
        # Voice call mode  
        voice_msg = {
            "message": question,
            "user_id": "test_user",
            "is_voice_call": True
        }
        
        async with session.post('http://localhost:8004/chat',
                                json=voice_msg) as response:
            voice_data = await response.json()
        
        print(f"Question: {question}")
        print()
        print(f"📝 Normal Mode ({len(normal_data['response'])} chars):")
        print(f"   {normal_data['response']}")
        print()
        print(f"📞 Voice Call Mode ({len(voice_data['response'])} chars):")
        print(f"   {voice_data['response']}")
        print()

async def main():
    print("🧪 Testing Cyra's Improved Personality & Response Modes")
    print("🌐 Server: http://localhost:8004")
    print()
    
    try:
        await test_normal_chat()
        await test_voice_call_mode()
        await test_comparison()
        
        print("✅ All tests completed!")
        print()
        print("💡 Key Improvements:")
        print("   • Friendlier, more casual tone")
        print("   • Shorter responses in voice call mode")
        print("   • Better conversational flow")
        print("   • Context-aware response length")
        
    except Exception as e:
        print(f"❌ Error testing: {e}")
        print("Make sure Cyra is running on http://localhost:8004")

if __name__ == "__main__":
    asyncio.run(main())
