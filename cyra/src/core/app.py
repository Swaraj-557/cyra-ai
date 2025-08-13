"""
Cyra AI Assistant - Main FastAPI Application
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from datetime import datetime
import uvicorn

from src.core.config import get_settings
from src.core.ai_brain import AIBrain
from src.speech.speech_service import SpeechService
from src.tools.tool_manager import ToolManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    response: str
    tool_calls: List[dict] = []
    conversation_id: int
    timestamp: datetime = datetime.now()

class TextToSpeechRequest(BaseModel):
    text: str
    voice: Optional[str] = None

class PasswordRequest(BaseModel):
    length: int = 16
    include_uppercase: bool = True
    include_lowercase: bool = True
    include_digits: bool = True
    include_special: bool = True
    exclude_ambiguous: bool = False
    count: int = 1

class PasswordStrengthRequest(BaseModel):
    password: str

# Global instances
ai_brain: AIBrain = None
speech_service: SpeechService = None
tool_manager: ToolManager = None
active_connections: List[WebSocket] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global ai_brain, speech_service, tool_manager
    
    # Startup
    logger.info("🚀 Starting Cyra AI Assistant...")
    
    try:
        ai_brain = AIBrain()
        tool_manager = ToolManager()
        logger.info("✅ Core services initialized successfully")
        
        # Initialize speech service with error handling
        try:
            speech_service = SpeechService()
            logger.info("✅ Speech service initialized")
        except Exception as e:
            logger.warning(f"⚠️ Speech service unavailable: {e}")
            speech_service = None
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize core services: {e}")
        raise e
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Cyra AI Assistant...")

# Create FastAPI app
app = FastAPI(
    title="Cyra AI Assistant",
    description="A sophisticated AI-powered cybersecurity assistant",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple authentication (for demonstration - use proper auth in production)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # In production, validate JWT token here
    return {"user_id": "authenticated_user", "username": "demo"}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cyra AI Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
            h1 { text-align: center; margin-bottom: 30px; }
            .chat-container { background: rgba(255,255,255,0.9); color: #333; padding: 20px; border-radius: 10px; margin-bottom: 20px; height: 400px; overflow-y: auto; }
            .input-container { display: flex; gap: 10px; }
            input { flex: 1; padding: 12px; border: none; border-radius: 8px; font-size: 16px; }
            button { padding: 12px 24px; background: #4CAF50; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; }
            button:hover { background: #45a049; }
            .message { margin: 10px 0; padding: 10px; border-radius: 8px; }
            .user-message { background: #e3f2fd; text-align: right; }
            .bot-message { background: #f3e5f5; }
            .api-info { margin-top: 30px; background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; }
            .api-info h3 { margin-top: 0; }
            .endpoint { background: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; margin: 5px 0; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Cyra AI Assistant</h1>
            <p style="text-align: center; margin-bottom: 30px;">Your sophisticated AI-powered cybersecurity assistant</p>
            
            <div class="chat-container" id="chatContainer">
                <div class="bot-message">
                    <strong>Cyra:</strong> Hello! I'm Cyra, your AI cybersecurity assistant. I can help you with:
                    <ul>
                        <li>🔐 Generating secure passwords and passphrases</li>
                        <li>🔍 Analyzing password strength</li>
                        <li>🌐 Network security advice</li>
                        <li>📚 Cybersecurity education and best practices</li>
                        <li>🛠️ Security tool recommendations</li>
                    </ul>
                    Try asking me: "Generate a strong password" or "How can I protect myself from phishing?"
                </div>
            </div>
            
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Ask me anything about cybersecurity..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
                <button onclick="toggleListening()" id="voiceButton">🎤 Voice</button>
            </div>
            
            <div class="api-info">
                <h3>🔌 API Endpoints</h3>
                <div class="endpoint">POST /chat - Send a message to Cyra</div>
                <div class="endpoint">POST /tools/password/generate - Generate secure passwords</div>
                <div class="endpoint">POST /tools/password/strength - Analyze password strength</div>
                <div class="endpoint">POST /speech/tts - Convert text to speech</div>
                <div class="endpoint">GET /health - Check service health</div>
                <div class="endpoint">WebSocket /ws - Real-time chat connection</div>
            </div>
        </div>
        
        <script>
            let isListening = false;
            
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;
                
                addMessage('user', message);
                input.value = '';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message, user_id: 'web_user' })
                    });
                    const data = await response.json();
                    addMessage('bot', data.response);
                    
                    if (data.tool_calls && data.tool_calls.length > 0) {
                        data.tool_calls.forEach(tool => {
                            addMessage('bot', `🔧 Tool executed: ${tool.tool_name}`, true);
                        });
                    }
                } catch (error) {
                    addMessage('bot', 'Sorry, I encountered an error. Please try again.');
                }
            }
            
            function addMessage(sender, message, isToolResult = false) {
                const container = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = sender === 'user' ? 'message user-message' : 'message bot-message';
                
                if (isToolResult) {
                    messageDiv.innerHTML = `<strong>System:</strong> ${message}`;
                } else {
                    messageDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Cyra'}:</strong> ${message}`;
                }
                
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            function toggleListening() {
                const button = document.getElementById('voiceButton');
                if (isListening) {
                    button.textContent = '🎤 Voice';
                    isListening = false;
                } else {
                    button.textContent = '🛑 Stop';
                    isListening = true;
                    // Voice recognition would be implemented here
                    setTimeout(() => {
                        button.textContent = '🎤 Voice';
                        isListening = false;
                    }, 3000);
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatMessage):
    """Process a chat message with Cyra"""
    try:
        result = await ai_brain.process_message(request.message, request.user_id)
        return ChatResponse(
            response=result["response"],
            tool_calls=result.get("tool_calls", []),
            conversation_id=result.get("conversation_id", 0)
        )
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/password/generate")
async def generate_password(request: PasswordRequest):
    """Generate secure passwords"""
    try:
        result = await tool_manager.execute_tool(
            "generate_password",
            request.dict(),
            "api_user"
        )
        return result
    except Exception as e:
        logger.error(f"Password generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/password/strength")
async def check_password_strength(request: PasswordStrengthRequest):
    """Analyze password strength"""
    try:
        result = await tool_manager.execute_tool(
            "assess_password_strength",
            {"password": request.password},
            "api_user"
        )
        return result
    except Exception as e:
        logger.error(f"Password strength check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speech/tts")
async def text_to_speech(request: TextToSpeechRequest):
    """Convert text to speech"""
    try:
        if not speech_service:
            return {"success": False, "message": "Speech service not available"}
            
        audio_data = await speech_service.text_to_speech(request.text)
        if audio_data:
            # In production, you might want to save this to a file and return a URL
            return {"success": True, "message": "Audio generated successfully", "size": len(audio_data)}
        else:
            return {"success": False, "message": "Failed to generate audio"}
    except Exception as e:
        logger.error(f"Text-to-speech error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = eval(data)  # In production, use json.loads() with proper validation
            
            result = await ai_brain.process_message(
                message_data.get("message", ""),
                message_data.get("user_id", "ws_user")
            )
            
            await websocket.send_text(str(result))  # In production, use json.dumps()
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("WebSocket client disconnected")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "ai_brain": ai_brain is not None,
            "speech_service": speech_service is not None,
            "tool_manager": tool_manager is not None
        },
        "timestamp": datetime.now(),
        "message": "Cyra AI Assistant is running"
    }

@app.get("/tools")
async def list_tools():
    """List available cybersecurity tools"""
    return {
        "tools": tool_manager.get_tool_list(),
        "descriptions": "Use the /chat endpoint to interact with tools through natural language"
    }

@app.get("/cybersecurity/advice/{topic}")
async def get_security_advice(topic: str):
    """Get cybersecurity advice on a specific topic"""
    try:
        result = await tool_manager.execute_tool(
            "get_security_advice",
            {"topic": topic},
            "api_user"
        )
        return result
    except Exception as e:
        logger.error(f"Security advice error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "src.core.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
