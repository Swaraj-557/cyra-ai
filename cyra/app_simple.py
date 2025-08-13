"""
Cyra AI Assistant - Main FastAPI Application (No Speech Version)
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import uvicorn

from src.core.config import get_settings
from src.core.ai_brain import AIBrain
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
tool_manager: ToolManager = None
active_connections: List[WebSocket] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global ai_brain, tool_manager
    
    # Startup
    logger.info("🚀 Starting Cyra AI Assistant...")
    
    try:
        ai_brain = AIBrain()
        tool_manager = ToolManager()
        logger.info("✅ Core services initialized successfully")
            
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

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cyra AI Assistant</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            
            .header {
                text-align: center;
                padding: 30px 0;
                backdrop-filter: blur(10px);
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                margin-bottom: 30px;
            }
            
            .header h1 {
                font-size: 3rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
            }
            
            .main-content {
                display: grid;
                grid-template-columns: 1fr 400px;
                gap: 30px;
                flex: 1;
            }
            
            .chat-section {
                background: rgba(255,255,255,0.95);
                color: #333;
                border-radius: 20px;
                padding: 30px;
                display: flex;
                flex-direction: column;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }
            
            .chat-container {
                flex: 1;
                overflow-y: auto;
                margin-bottom: 20px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 15px;
                min-height: 400px;
            }
            
            .message {
                margin: 15px 0;
                padding: 15px 20px;
                border-radius: 20px;
                max-width: 80%;
                animation: fadeIn 0.3s ease-in;
            }
            
            .user-message {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                margin-left: auto;
                text-align: right;
            }
            
            .bot-message {
                background: white;
                color: #333;
                border: 2px solid #e9ecef;
                margin-right: auto;
            }
            
            .input-container {
                display: flex;
                gap: 15px;
                align-items: stretch;
            }
            
            .message-input {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #e9ecef;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }
            
            .message-input:focus {
                border-color: #667eea;
            }
            
            .send-btn {
                padding: 15px 30px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: transform 0.2s;
            }
            
            .send-btn:hover {
                transform: translateY(-2px);
            }
            
            .sidebar {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            
            .info-card {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 25px;
                border: 1px solid rgba(255,255,255,0.2);
            }
            
            .info-card h3 {
                margin-bottom: 15px;
                font-size: 1.3rem;
            }
            
            .feature-list {
                list-style: none;
            }
            
            .feature-list li {
                padding: 8px 0;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .feature-list li::before {
                content: "🛡️";
                font-size: 1.2rem;
            }
            
            .api-endpoint {
                background: rgba(0,0,0,0.2);
                padding: 10px 15px;
                border-radius: 10px;
                margin: 5px 0;
                font-family: 'Courier New', monospace;
                font-size: 0.9rem;
            }
            
            .status-indicator {
                display: inline-block;
                width: 10px;
                height: 10px;
                background: #28a745;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            @media (max-width: 768px) {
                .main-content {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 2rem;
                }
            }
            
            .loading {
                display: none;
                color: #667eea;
            }
            
            .loading.active {
                display: inline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ Cyra AI Assistant</h1>
                <p><span class="status-indicator"></span>Your sophisticated AI-powered cybersecurity companion</p>
            </div>
            
            <div class="main-content">
                <div class="chat-section">
                    <div class="chat-container" id="chatContainer">
                        <div class="bot-message">
                            <strong>Cyra:</strong> Hello! I'm Cyra, your AI cybersecurity assistant. I can help you with:
                            <ul style="margin-top: 10px; padding-left: 20px;">
                                <li>🔐 Generating secure passwords and passphrases</li>
                                <li>🔍 Analyzing password strength and security</li>
                                <li>🌐 Network security advice and best practices</li>
                                <li>📚 Cybersecurity education and guidance</li>
                                <li>🛠️ Security tool recommendations</li>
                            </ul>
                            <p style="margin-top: 15px;"><strong>Try asking:</strong> "Generate a strong password" or "How can I protect myself from phishing?"</p>
                        </div>
                    </div>
                    
                    <div class="input-container">
                        <input type="text" class="message-input" id="messageInput" placeholder="Ask me anything about cybersecurity..." onkeypress="handleKeyPress(event)">
                        <button class="send-btn" onclick="sendMessage()">
                            <span id="sendText">Send</span>
                            <span class="loading" id="loadingText">●●●</span>
                        </button>
                    </div>
                </div>
                
                <div class="sidebar">
                    <div class="info-card">
                        <h3>🚀 Features</h3>
                        <ul class="feature-list">
                            <li>Password Generation</li>
                            <li>Security Analysis</li>
                            <li>Threat Education</li>
                            <li>Best Practices</li>
                            <li>Real-time Chat</li>
                        </ul>
                    </div>
                    
                    <div class="info-card">
                        <h3>🔌 API Endpoints</h3>
                        <div class="api-endpoint">POST /chat</div>
                        <div class="api-endpoint">POST /tools/password/generate</div>
                        <div class="api-endpoint">POST /tools/password/strength</div>
                        <div class="api-endpoint">GET /health</div>
                        <div class="api-endpoint">GET /docs</div>
                    </div>
                    
                    <div class="info-card">
                        <h3>📖 Quick Links</h3>
                        <a href="/docs" style="color: white; text-decoration: none; display: block; padding: 8px 0;">📚 API Documentation</a>
                        <a href="/health" style="color: white; text-decoration: none; display: block; padding: 8px 0;">💚 Health Check</a>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let isLoading = false;
            
            async function sendMessage() {
                if (isLoading) return;
                
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;
                
                setLoading(true);
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
                            if (tool.result && tool.result.result) {
                                const result = tool.result.result;
                                if (result.password) {
                                    addMessage('bot', `🔧 Generated password: <code style="background: #f0f0f0; padding: 2px 6px; border-radius: 4px;">${result.password}</code>`, true);
                                }
                                if (result.passwords) {
                                    const passwords = result.passwords.map(p => `<code style="background: #f0f0f0; padding: 2px 6px; border-radius: 4px;">${p.password}</code> (${p.strength_level})`).join('<br>');
                                    addMessage('bot', `🔧 Generated passwords:<br>${passwords}`, true);
                                }
                            }
                        });
                    }
                } catch (error) {
                    addMessage('bot', 'Sorry, I encountered an error. Please try again.');
                } finally {
                    setLoading(false);
                }
            }
            
            function addMessage(sender, message, isToolResult = false) {
                const container = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = sender === 'user' ? 'message user-message' : 'message bot-message';
                
                if (isToolResult) {
                    messageDiv.innerHTML = `<strong>🔧 Tool Result:</strong><br>${message}`;
                } else {
                    messageDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Cyra'}:</strong> ${message}`;
                }
                
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }
            
            function setLoading(loading) {
                isLoading = loading;
                const sendText = document.getElementById('sendText');
                const loadingText = document.getElementById('loadingText');
                
                if (loading) {
                    sendText.style.display = 'none';
                    loadingText.classList.add('active');
                } else {
                    sendText.style.display = 'inline';
                    loadingText.classList.remove('active');
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter' && !isLoading) {
                    sendMessage();
                }
            }
            
            // Auto-focus input
            document.getElementById('messageInput').focus();
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "ai_brain": ai_brain is not None,
            "tool_manager": tool_manager is not None,
            "speech_service": False  # Disabled for now
        },
        "timestamp": datetime.now(),
        "message": "Cyra AI Assistant is running (Speech services disabled)"
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
        "app_simple:app",
        host=settings.host,
        port=settings.port,
        reload=False,  # Disable reload for direct execution
        log_level=settings.log_level.lower()
    )
