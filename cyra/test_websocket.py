"""
WebSocket Test for Cyra Advanced
================================

This script tests the WebSocket functionality to ensure real-time communication works.
"""
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8003/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected successfully!")
            
            # Send a test message
            test_message = {
                "message": "Hello Cyra, this is a WebSocket test. Can you respond?",
                "user_id": "test_user",
                "conversation_id": "test_conversation"
            }
            
            print("📤 Sending test message...")
            await websocket.send(json.dumps(test_message))
            
            # Wait for response
            print("⏳ Waiting for response...")
            response = await websocket.recv()
            data = json.loads(response)
            
            print("📥 Received response:")
            print(f"   Type: {data.get('type')}")
            print(f"   Message: {data.get('message')}")
            
            print("✅ WebSocket test completed successfully!")
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Cyra WebSocket Connection...")
    print("📍 Server: ws://localhost:8003/ws")
    print()
    
    asyncio.run(test_websocket())
