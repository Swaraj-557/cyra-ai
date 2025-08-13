"""
Cyra AI Assistant - Professional Edition with Icons8 Integration
Error-free, polished application with premium icons and enhanced features
"""
import asyncio
import logging
import os
import json
import base64
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
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

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    user_id: str = "default_user"
    conversation_id: Optional[str] = None
    is_voice_call: bool = False

class VoiceMessage(BaseModel):
    audio_data: str
    user_id: str = "default_user"
    format: str = "webm"

# Global instances
ai_brain: AIBrain = None
tool_manager: ToolManager = None
active_connections: Dict[str, WebSocket] = {}
conversations: Dict[str, List[Dict]] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global ai_brain, tool_manager
    
    logger.info("🚀 Starting Cyra AI Assistant Professional...")
    
    try:
        # Initialize AI Brain
        ai_brain = AIBrain()
        
        # Initialize Tool Manager
        tool_manager = ToolManager()
        
        logger.info("✅ Core services initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {e}")
        raise
    
    yield
    
    logger.info("🛑 Shutting down Cyra AI Assistant Professional...")

# Create FastAPI app
app = FastAPI(
    title="Cyra AI Assistant Professional",
    description="Advanced cybersecurity assistant with voice features and Icons8 integration",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("assets"):
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """Serve the main application page with Icons8 integration"""
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cyra AI Assistant Professional</title>
        <link rel="icon" type="image/x-icon" href="/assets/icons/favicon.ico">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
                color: #ffffff;
                overflow: hidden;
                height: 100vh;
            }}
            
            .app-container {{
                display: flex;
                height: 100vh;
                position: relative;
            }}
            
            /* Animated Background */
            .background-animation {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 0;
            }}
            
            .floating-icon {{
                position: absolute;
                opacity: 0.1;
                animation: float 6s ease-in-out infinite;
            }}
            
            @keyframes float {{
                0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
                50% {{ transform: translateY(-20px) rotate(5deg); }}
            }}
            
            /* Sidebar */
            .sidebar {{
                width: 260px;
                background: rgba(20, 20, 32, 0.95);
                backdrop-filter: blur(20px);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                flex-direction: column;
                position: relative;
                z-index: 10;
                box-shadow: 0 0 30px rgba(0, 0, 0, 0.3);
            }}
            
            .sidebar-header {{
                padding: 20px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .logo {{
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 20px;
            }}
            
            .logo-icon {{
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                font-weight: bold;
            }}
            
            .logo-text {{
                font-size: 24px;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .new-chat-btn {{
                width: 100%;
                padding: 12px 16px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 12px;
                color: white;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }}
            
            .new-chat-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }}
            
            .conversations-list {{
                flex: 1;
                padding: 20px;
                overflow-y: auto;
            }}
            
            .conversation-item {{
                padding: 12px 16px;
                border-radius: 8px;
                cursor: pointer;
                margin-bottom: 8px;
                transition: all 0.2s ease;
                border: 1px solid transparent;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .conversation-item:hover {{
                background: rgba(255, 255, 255, 0.05);
                border-color: rgba(255, 255, 255, 0.1);
            }}
            
            .conversation-item.active {{
                background: rgba(102, 126, 234, 0.2);
                border-color: rgba(102, 126, 234, 0.3);
            }}
            
            .sidebar-footer {{
                padding: 20px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .user-info {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            
            .user-avatar {{
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
            }}
            
            /* Main Content */
            .main-content {{
                flex: 1;
                display: flex;
                flex-direction: column;
                position: relative;
                z-index: 10;
            }}
            
            .chat-header {{
                padding: 20px 30px;
                background: rgba(20, 20, 32, 0.95);
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
            }}
            
            .chat-title {{
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 20px;
                font-weight: 600;
            }}
            
            .title-icon {{
                width: 32px;
                height: 32px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .voice-controls {{
                display: flex;
                gap: 12px;
            }}
            
            .voice-btn {{
                padding: 10px 16px;
                border: none;
                border-radius: 10px;
                color: white;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            
            .voice-btn::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }}
            
            .voice-btn:hover::before {{
                left: 100%;
            }}
            
            .voice-btn.record {{
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            }}
            
            .voice-btn.speak {{
                background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
                box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
            }}
            
            .voice-btn.live-call {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
            }}
            
            .voice-btn.recording {{
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                animation: pulse 1.5s infinite;
            }}
            
            .voice-btn.active {{
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                transform: scale(1.05);
            }}
            
            .voice-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
            }}
            
            /* Chat Messages */
            .chat-messages {{
                flex: 1;
                padding: 30px;
                overflow-y: auto;
                scroll-behavior: smooth;
            }}
            
            .message {{
                display: flex;
                gap: 15px;
                margin-bottom: 25px;
                animation: fadeIn 0.5s ease-out;
            }}
            
            .message.user {{
                flex-direction: row-reverse;
            }}
            
            .message-avatar {{
                width: 45px;
                height: 45px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                font-size: 16px;
                flex-shrink: 0;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }}
            
            .message.user .message-avatar {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            
            .message.assistant .message-avatar {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            }}
            
            .message-content {{
                flex: 1;
                max-width: 70%;
            }}
            
            .message.user .message-content {{
                text-align: right;
            }}
            
            .message-text {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 16px 20px;
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                line-height: 1.6;
                margin-bottom: 8px;
                position: relative;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }}
            
            .message.user .message-text {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 18px 18px 4px 18px;
            }}
            
            .message.assistant .message-text {{
                background: rgba(255, 255, 255, 0.05);
                border-radius: 18px 18px 18px 4px;
            }}
            
            .message-time {{
                font-size: 12px;
                color: rgba(255, 255, 255, 0.6);
                margin-top: 4px;
            }}
            
            .typing-indicator {{
                display: none;
                align-items: center;
                gap: 15px;
                margin-bottom: 25px;
                animation: fadeIn 0.3s ease-out;
            }}
            
            .typing-dots {{
                display: flex;
                gap: 4px;
                padding: 16px 20px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 18px 18px 18px 4px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .typing-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #10b981;
                animation: typing 1.4s infinite ease-in-out;
            }}
            
            .typing-dot:nth-child(2) {{ animation-delay: 0.2s; }}
            .typing-dot:nth-child(3) {{ animation-delay: 0.4s; }}
            
            @keyframes typing {{
                0%, 60%, 100% {{ transform: translateY(0); opacity: 0.3; }}
                30% {{ transform: translateY(-10px); opacity: 1; }}
            }}
            
            /* Input Area */
            .input-area {{
                padding: 20px 30px 30px;
                background: rgba(20, 20, 32, 0.95);
                backdrop-filter: blur(20px);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .input-container {{
                position: relative;
                max-width: 800px;
                margin: 0 auto;
            }}
            
            .message-input {{
                width: 100%;
                min-height: 56px;
                max-height: 150px;
                padding: 16px 60px 16px 20px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                color: #ffffff;
                font-size: 16px;
                font-family: inherit;
                resize: none;
                outline: none;
                transition: all 0.3s ease;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }}
            
            .message-input:focus {{
                border-color: rgba(102, 126, 234, 0.5);
                box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
            }}
            
            .message-input::placeholder {{
                color: rgba(255, 255, 255, 0.5);
            }}
            
            .send-btn {{
                position: absolute;
                right: 8px;
                top: 50%;
                transform: translateY(-50%);
                width: 44px;
                height: 44px;
                border: none;
                border-radius: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }}
            
            .send-btn:hover:not(:disabled) {{
                transform: translateY(-50%) scale(1.05);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }}
            
            .send-btn:disabled {{
                background: rgba(255, 255, 255, 0.1);
                cursor: not-allowed;
                box-shadow: none;
            }}
            
            /* Voice Status */
            .voice-status {{
                position: fixed;
                bottom: 120px;
                right: 30px;
                background: rgba(20, 20, 32, 0.95);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                padding: 16px 20px;
                display: none;
                align-items: center;
                gap: 12px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
                z-index: 1000;
                animation: slideIn 0.3s ease-out;
            }}
            
            .voice-status.active {{
                display: flex;
            }}
            
            @keyframes slideIn {{
                from {{ transform: translateX(100%); opacity: 0; }}
                to {{ transform: translateX(0); opacity: 1; }}
            }}
            
            .voice-indicator {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #ef4444;
                animation: pulse 1s infinite;
            }}
            
            .voice-text {{
                color: #ffffff;
                font-size: 14px;
                font-weight: 500;
            }}
            
            /* Mobile Responsive */
            @media (max-width: 768px) {{
                .sidebar {{
                    width: 100%;
                    position: fixed;
                    left: 0;
                    top: 0;
                    z-index: 1000;
                    transform: translateX(-100%);
                    transition: transform 0.3s ease;
                }}
                
                .sidebar.open {{
                    transform: translateX(0);
                }}
                
                .main-content {{
                    width: 100%;
                }}
                
                .chat-header {{
                    padding: 15px 20px;
                }}
                
                .voice-controls {{
                    gap: 8px;
                }}
                
                .voice-btn {{
                    padding: 8px 12px;
                    font-size: 12px;
                }}
                
                .chat-messages {{
                    padding: 20px;
                }}
                
                .message-content {{
                    max-width: 85%;
                }}
                
                .input-area {{
                    padding: 15px 20px 20px;
                }}
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {{
                width: 8px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: rgba(255, 255, 255, 0.05);
                border-radius: 4px;
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: rgba(255, 255, 255, 0.3);
            }}
            
            /* Code Highlighting */
            pre {{
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                padding: 15px;
                overflow-x: auto;
                margin: 10px 0;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            code {{
                background: rgba(0, 0, 0, 0.3);
                padding: 2px 6px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            /* Error States */
            .error-message {{
                background: rgba(239, 68, 68, 0.1);
                border: 1px solid rgba(239, 68, 68, 0.3);
                color: #fca5a5;
                padding: 12px 16px;
                border-radius: 8px;
                margin: 10px 0;
            }}
            
            .success-message {{
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.3);
                color: #6ee7b7;
                padding: 12px 16px;
                border-radius: 8px;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <!-- Animated Background -->
        <div class="background-animation">
            <div class="floating-icon" style="top: 10%; left: 5%;">🔐</div>
            <div class="floating-icon" style="top: 20%; right: 10%; animation-delay: 1s;">🛡️</div>
            <div class="floating-icon" style="bottom: 30%; left: 8%; animation-delay: 2s;">🔒</div>
            <div class="floating-icon" style="top: 60%; right: 15%; animation-delay: 3s;">🌐</div>
            <div class="floating-icon" style="bottom: 20%; right: 5%; animation-delay: 4s;">⚡</div>
        </div>
        
        <div class="app-container">
            <!-- Sidebar -->
            <div class="sidebar" id="sidebar">
                <div class="sidebar-header">
                    <div class="logo">
                        <div class="logo-icon">C</div>
                        <div class="logo-text">Cyra</div>
                    </div>
                    <button class="new-chat-btn" onclick="startNewChat()">
                        <i class="fas fa-plus"></i>
                        New conversation
                    </button>
                </div>
                
                <div class="conversations-list" id="conversationsList">
                    <!-- Conversations will be loaded here -->
                </div>
                
                <div class="sidebar-footer">
                    <div class="user-info">
                        <div class="user-avatar">U</div>
                        <div>
                            <div style="font-weight: 500;">Security Expert</div>
                            <div style="font-size: 12px; color: rgba(255,255,255,0.6);">Premium User</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Main Content -->
            <div class="main-content">
                <div class="chat-header">
                    <div class="chat-title">
                        <div class="title-icon">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        Cyra AI Assistant Professional
                    </div>
                    <div class="voice-controls">
                        <button class="voice-btn record" id="recordBtn" onclick="toggleRecording()">
                            <i class="fas fa-microphone"></i>
                            <span>Record</span>
                        </button>
                        <button class="voice-btn speak" id="speakBtn" onclick="toggleSpeech()">
                            <i class="fas fa-volume-up"></i>
                            <span>Speech</span>
                        </button>
                        <button class="voice-btn live-call" id="liveCallBtn" onclick="toggleLiveCall()">
                            <i class="fas fa-phone"></i>
                            <span>Live Call</span>
                        </button>
                    </div>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message assistant">
                        <div class="message-avatar">C</div>
                        <div class="message-content">
                            <div class="message-text">
                                Hey there! 👋 I'm Cyra, your friendly cybersecurity buddy! 
                                <br><br>
                                I can help you with:
                                <br>
                                🔐 <strong>Passwords</strong> - Generate & check them<br>
                                🛡️ <strong>Security Tips</strong> - Stay safe online<br>  
                                🎤 <strong>Voice Chat</strong> - Just talk to me!<br>
                                📞 <strong>Live Calls</strong> - Real conversations
                                <br><br>
                                Try saying: <em>"Hey Cyra, make me a password!"</em> 😊
                            </div>
                            <div class="message-time">Just now</div>
                        </div>
                    </div>
                </div>
                
                <div class="typing-indicator" id="typingIndicator">
                    <div class="message-avatar" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">C</div>
                    <div>
                        <div class="typing-dots">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                </div>
                
                <div class="input-area">
                    <div class="input-container">
                        <textarea 
                            class="message-input" 
                            id="messageInput" 
                            placeholder="Message Cyra..." 
                            rows="1"
                            onkeydown="handleKeyDown(event)"
                            oninput="autoResize(this)"
                        ></textarea>
                        <button class="send-btn" id="sendBtn" onclick="sendMessage()">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Voice Status Indicator -->
        <div class="voice-status" id="voiceStatus">
            <div class="voice-indicator"></div>
            <div class="voice-text" id="voiceStatusText">Listening...</div>
        </div>
        
        <script>
            // Global variables
            let isRecording = false;
            let isSpeechEnabled = false;
            let isLiveCallActive = false;
            let mediaRecorder = null;
            let audioChunks = [];
            let recognition = null;
            let currentConversationId = null;
            let websocket = null;
            
            // Initialize the application
            document.addEventListener('DOMContentLoaded', function() {{
                console.log('🚀 Initializing Cyra Professional...');
                initializeSpeechRecognition();
                initializeWebSocket();
                loadConversations();
                focusInput();
                console.log('✅ Cyra Professional initialized successfully');
            }});
            
            // WebSocket connection for real-time communication
            function initializeWebSocket() {{
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${{protocol}}//${{window.location.host}}/ws`;
                
                try {{
                    websocket = new WebSocket(wsUrl);
                    
                    websocket.onopen = function() {{
                        console.log('✅ WebSocket connected');
                    }};
                    
                    websocket.onmessage = function(event) {{
                        try {{
                            const data = JSON.parse(event.data);
                            if (data.type === 'response') {{
                                hideTypingIndicator();
                                addMessage('assistant', data.message);
                                if (isSpeechEnabled || isLiveCallActive) {{
                                    speakText(data.message);
                                }}
                            }}
                        }} catch (error) {{
                            console.error('❌ Error parsing WebSocket message:', error);
                        }}
                    }};
                    
                    websocket.onclose = function() {{
                        console.log('🔄 WebSocket disconnected, attempting to reconnect...');
                        setTimeout(initializeWebSocket, 3000);
                    }};
                    
                    websocket.onerror = function(error) {{
                        console.error('❌ WebSocket error:', error);
                    }};
                    
                }} catch (error) {{
                    console.warn('⚠️ WebSocket not available, using HTTP fallback');
                }}
            }}
            
            // Speech Recognition Setup
            function initializeSpeechRecognition() {{
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    recognition = new SpeechRecognition();
                    recognition.continuous = true;
                    recognition.interimResults = true;
                    recognition.lang = 'en-US';
                    
                    recognition.onstart = function() {{
                        console.log('🎤 Speech recognition started');
                    }};
                    
                    recognition.onresult = function(event) {{
                        let finalTranscript = '';
                        let interimTranscript = '';
                        
                        for (let i = event.resultIndex; i < event.results.length; ++i) {{
                            if (event.results[i].isFinal) {{
                                finalTranscript += event.results[i][0].transcript;
                            }} else {{
                                interimTranscript += event.results[i][0].transcript;
                            }}
                        }}
                        
                        if (finalTranscript) {{
                            const input = document.getElementById('messageInput');
                            input.value = finalTranscript.trim();
                            autoResize(input);
                            if (isLiveCallActive) {{
                                sendMessage();
                            }}
                        }}
                    }};
                    
                    recognition.onerror = function(event) {{
                        console.error('❌ Speech recognition error:', event.error);
                        showErrorMessage('Speech recognition error: ' + event.error);
                        stopRecording();
                    }};
                    
                    recognition.onend = function() {{
                        if (isRecording || isLiveCallActive) {{
                            try {{
                                recognition.start();
                            }} catch (error) {{
                                console.error('❌ Error restarting recognition:', error);
                            }}
                        }}
                    }};
                    
                    console.log('✅ Speech recognition initialized');
                }} else {{
                    console.warn('⚠️ Speech recognition not supported in this browser');
                    showErrorMessage('Speech recognition not supported in this browser');
                }}
            }}
            
            // Voice Recording Functions
            function toggleRecording() {{
                if (isRecording) {{
                    stopRecording();
                }} else {{
                    startRecording();
                }}
            }}
            
            function startRecording() {{
                if (!recognition) {{
                    showErrorMessage('Speech recognition not available');
                    return;
                }}
                
                try {{
                    isRecording = true;
                    const recordBtn = document.getElementById('recordBtn');
                    recordBtn.classList.add('recording');
                    recordBtn.innerHTML = '<i class="fas fa-stop"></i><span>Stop</span>';
                    
                    showVoiceStatus('🎤 Listening...');
                    recognition.start();
                    console.log('🎤 Recording started');
                }} catch (error) {{
                    console.error('❌ Error starting recording:', error);
                    showErrorMessage('Failed to start recording');
                    isRecording = false;
                }}
            }}
            
            function stopRecording() {{
                try {{
                    isRecording = false;
                    const recordBtn = document.getElementById('recordBtn');
                    recordBtn.classList.remove('recording');
                    recordBtn.innerHTML = '<i class="fas fa-microphone"></i><span>Record</span>';
                    
                    hideVoiceStatus();
                    if (recognition) {{
                        recognition.stop();
                    }}
                    console.log('🎤 Recording stopped');
                }} catch (error) {{
                    console.error('❌ Error stopping recording:', error);
                }}
            }}
            
            // Speech Synthesis Functions
            function toggleSpeech() {{
                isSpeechEnabled = !isSpeechEnabled;
                const speakBtn = document.getElementById('speakBtn');
                
                if (isSpeechEnabled) {{
                    speakBtn.classList.add('active');
                    speakBtn.innerHTML = '<i class="fas fa-volume-mute"></i><span>Mute</span>';
                    console.log('🔊 Speech enabled');
                }} else {{
                    speakBtn.classList.remove('active');
                    speakBtn.innerHTML = '<i class="fas fa-volume-up"></i><span>Speech</span>';
                    speechSynthesis.cancel(); // Stop any ongoing speech
                    console.log('🔇 Speech disabled');
                }}
            }}
            
            function speakText(text) {{
                if (!isSpeechEnabled && !isLiveCallActive) return;
                if (!('speechSynthesis' in window)) {{
                    console.warn('⚠️ Speech synthesis not supported');
                    return;
                }}
                
                try {{
                    // Stop any ongoing speech
                    speechSynthesis.cancel();
                    
                    // Clean text for speech (remove markdown and HTML)
                    const cleanText = text
                        .replace(/\*\*(.*?)\*\*/g, '$1')
                        .replace(/\*(.*?)\*/g, '$1')
                        .replace(/<[^>]*>/g, '')
                        .replace(/🔐|🛡️|🎤|📞|😊|👋/g, '');
                    
                    const utterance = new SpeechSynthesisUtterance(cleanText);
                    utterance.rate = 0.9;
                    utterance.pitch = 1.1;
                    utterance.volume = 0.8;
                    
                    // Try to use a female voice
                    const voices = speechSynthesis.getVoices();
                    const femaleVoice = voices.find(voice => 
                        voice.name.includes('Female') || 
                        voice.name.includes('Zira') || 
                        voice.name.includes('Aria') ||
                        voice.name.includes('Samantha') ||
                        voice.gender === 'female'
                    );
                    
                    if (femaleVoice) {{
                        utterance.voice = femaleVoice;
                    }}
                    
                    utterance.onstart = function() {{
                        console.log('🗣️ Speech started');
                    }};
                    
                    utterance.onend = function() {{
                        console.log('🗣️ Speech ended');
                    }};
                    
                    utterance.onerror = function(event) {{
                        console.error('❌ Speech synthesis error:', event.error);
                    }};
                    
                    speechSynthesis.speak(utterance);
                }} catch (error) {{
                    console.error('❌ Error in speech synthesis:', error);
                }}
            }}
            
            // Live Call Functions
            function toggleLiveCall() {{
                if (isLiveCallActive) {{
                    stopLiveCall();
                }} else {{
                    startLiveCall();
                }}
            }}
            
            function startLiveCall() {{
                if (!recognition) {{
                    showErrorMessage('Speech recognition not available for live calls');
                    return;
                }}
                
                try {{
                    isLiveCallActive = true;
                    isSpeechEnabled = true;
                    
                    const liveCallBtn = document.getElementById('liveCallBtn');
                    liveCallBtn.classList.add('active');
                    liveCallBtn.innerHTML = '<i class="fas fa-phone-slash"></i><span>End Call</span>';
                    
                    const speakBtn = document.getElementById('speakBtn');
                    speakBtn.classList.add('active');
                    speakBtn.innerHTML = '<i class="fas fa-volume-mute"></i><span>Mute</span>';
                    
                    showVoiceStatus('📞 Live call active - Speak naturally');
                    recognition.start();
                    
                    addMessage('system', '📞 Live call started. Speak naturally to Cyra.');
                    console.log('📞 Live call started');
                }} catch (error) {{
                    console.error('❌ Error starting live call:', error);
                    showErrorMessage('Failed to start live call');
                    isLiveCallActive = false;
                }}
            }}
            
            function stopLiveCall() {{
                try {{
                    isLiveCallActive = false;
                    
                    const liveCallBtn = document.getElementById('liveCallBtn');
                    liveCallBtn.classList.remove('active');
                    liveCallBtn.innerHTML = '<i class="fas fa-phone"></i><span>Live Call</span>';
                    
                    hideVoiceStatus();
                    if (recognition) {{
                        recognition.stop();
                    }}
                    
                    addMessage('system', '📞 Live call ended.');
                    console.log('📞 Live call ended');
                }} catch (error) {{
                    console.error('❌ Error stopping live call:', error);
                }}
            }}
            
            // Voice Status Functions
            function showVoiceStatus(text) {{
                try {{
                    const voiceStatus = document.getElementById('voiceStatus');
                    const voiceStatusText = document.getElementById('voiceStatusText');
                    voiceStatusText.textContent = text;
                    voiceStatus.classList.add('active');
                }} catch (error) {{
                    console.error('❌ Error showing voice status:', error);
                }}
            }}
            
            function hideVoiceStatus() {{
                try {{
                    const voiceStatus = document.getElementById('voiceStatus');
                    voiceStatus.classList.remove('active');
                }} catch (error) {{
                    console.error('❌ Error hiding voice status:', error);
                }}
            }}
            
            // Message Functions
            async function sendMessage() {{
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                try {{
                    // Add user message
                    addMessage('user', message);
                    input.value = '';
                    autoResize(input);
                    
                    // Show typing indicator
                    showTypingIndicator();
                    
                    const response = await fetch('/chat', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ 
                            message, 
                            user_id: 'web_user',
                            conversation_id: currentConversationId,
                            is_voice_call: isLiveCallActive
                        }})
                    }});
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    
                    const data = await response.json();
                    
                    // Hide typing indicator
                    hideTypingIndicator();
                    
                    // Add assistant response
                    addMessage('assistant', data.response);
                    
                    // Handle tool calls
                    if (data.tool_calls && data.tool_calls.length > 0) {{
                        data.tool_calls.forEach(tool => {{
                            if (tool.result && tool.result.result) {{
                                displayToolResult(tool);
                            }}
                        }});
                    }}
                    
                    // Speak response if enabled
                    if (isSpeechEnabled || isLiveCallActive) {{
                        speakText(data.response);
                    }}
                    
                }} catch (error) {{
                    console.error('❌ Error sending message:', error);
                    hideTypingIndicator();
                    addMessage('assistant', '❌ Sorry, I encountered an error. Please try again.');
                    showErrorMessage('Failed to send message: ' + error.message);
                }}
                
                focusInput();
            }}
            
            function addMessage(sender, content, isSystem = false) {{
                try {{
                    const messagesContainer = document.getElementById('chatMessages');
                    const messageDiv = document.createElement('div');
                    
                    if (isSystem || sender === 'system') {{
                        messageDiv.className = 'message system';
                        messageDiv.innerHTML = `
                            <div style="text-align: center; color: rgba(255,255,255,0.7); font-style: italic; margin: 10px 0; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px;">
                                ${{content}}
                            </div>
                        `;
                    }} else {{
                        messageDiv.className = `message ${{sender}}`;
                        const avatar = sender === 'user' ? 'U' : 'C';
                        const time = new Date().toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
                        
                        messageDiv.innerHTML = `
                            <div class="message-avatar">${{avatar}}</div>
                            <div class="message-content">
                                <div class="message-text">${{formatMessage(content)}}</div>
                                <div class="message-time">${{time}}</div>
                            </div>
                        `;
                    }}
                    
                    messagesContainer.appendChild(messageDiv);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }} catch (error) {{
                    console.error('❌ Error adding message:', error);
                }}
            }}
            
            function formatMessage(content) {{
                try {{
                    // Basic markdown-like formatting with improved regex
                    content = content.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
                    content = content.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
                    content = content.replace(/`(.*?)`/g, '<code>$1</code>');
                    content = content.replace(/\\n/g, '<br>');
                    return content;
                }} catch (error) {{
                    console.error('❌ Error formatting message:', error);
                    return content; // Return original content if formatting fails
                }}
            }}
            
            function displayToolResult(tool) {{
                try {{
                    const result = tool.result.result;
                    let message = '';
                    
                    if (result.password) {{
                        message = `🔧 Generated password: <code>${{result.password}}</code><br>Strength: ${{result.strength.level}} (${{result.strength.score}}/100)`;
                    }} else if (result.passwords) {{
                        message = '🔧 Generated passwords:<br>';
                        result.passwords.forEach(p => {{
                            message += `<code>${{p.password}}</code> (${{p.strength_level}})<br>`;
                        }});
                    }} else if (result.score !== undefined) {{
                        message = `🔍 Password analysis: ${{result.level}} (${{result.score}}/100)<br>Estimated crack time: ${{result.estimated_crack_time}}`;
                    }}
                    
                    if (message) {{
                        addMessage('assistant', message);
                    }}
                }} catch (error) {{
                    console.error('❌ Error displaying tool result:', error);
                }}
            }}
            
            function showTypingIndicator() {{
                try {{
                    document.getElementById('typingIndicator').style.display = 'flex';
                    const messagesContainer = document.getElementById('chatMessages');
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }} catch (error) {{
                    console.error('❌ Error showing typing indicator:', error);
                }}
            }}
            
            function hideTypingIndicator() {{
                try {{
                    document.getElementById('typingIndicator').style.display = 'none';
                }} catch (error) {{
                    console.error('❌ Error hiding typing indicator:', error);
                }}
            }}
            
            // Input Handling
            function handleKeyDown(event) {{
                try {{
                    if (event.key === 'Enter' && !event.shiftKey) {{
                        event.preventDefault();
                        sendMessage();
                    }}
                }} catch (error) {{
                    console.error('❌ Error handling key down:', error);
                }}
            }}
            
            function autoResize(textarea) {{
                try {{
                    textarea.style.height = 'auto';
                    textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
                }} catch (error) {{
                    console.error('❌ Error auto-resizing textarea:', error);
                }}
            }}
            
            function focusInput() {{
                try {{
                    document.getElementById('messageInput').focus();
                }} catch (error) {{
                    console.error('❌ Error focusing input:', error);
                }}
            }}
            
            // Conversation Management
            function startNewChat() {{
                try {{
                    currentConversationId = Date.now().toString();
                    document.getElementById('chatMessages').innerHTML = '';
                    
                    // Add welcome message
                    addMessage('assistant', `Hey there! 👋 I'm Cyra, your friendly cybersecurity buddy!

I can help you with:
🔐 **Passwords** - Generate & check them
🛡️ **Security Tips** - Stay safe online  
🎤 **Voice Chat** - Just talk to me!
📞 **Live Calls** - Real conversations

Try saying: *"Hey Cyra, make me a password!"* 😊`);
                    
                    focusInput();
                    console.log('🆕 New chat started');
                }} catch (error) {{
                    console.error('❌ Error starting new chat:', error);
                }}
            }}
            
            function loadConversations() {{
                try {{
                    const conversationsList = document.getElementById('conversationsList');
                    conversationsList.innerHTML = `
                        <div class="conversation-item active">
                            <i class="fas fa-comments"></i>
                            Current Conversation
                        </div>
                    `;
                }} catch (error) {{
                    console.error('❌ Error loading conversations:', error);
                }}
            }}
            
            // Error and Success Messages
            function showErrorMessage(message) {{
                try {{
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error-message';
                    errorDiv.textContent = message;
                    
                    const messagesContainer = document.getElementById('chatMessages');
                    messagesContainer.appendChild(errorDiv);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    
                    // Auto-remove after 5 seconds
                    setTimeout(() => {{
                        if (errorDiv.parentNode) {{
                            errorDiv.parentNode.removeChild(errorDiv);
                        }}
                    }}, 5000);
                }} catch (error) {{
                    console.error('❌ Error showing error message:', error);
                }}
            }}
            
            function showSuccessMessage(message) {{
                try {{
                    const successDiv = document.createElement('div');
                    successDiv.className = 'success-message';
                    successDiv.textContent = message;
                    
                    const messagesContainer = document.getElementById('chatMessages');
                    messagesContainer.appendChild(successDiv);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    
                    // Auto-remove after 3 seconds
                    setTimeout(() => {{
                        if (successDiv.parentNode) {{
                            successDiv.parentNode.removeChild(successDiv);
                        }}
                    }}, 3000);
                }} catch (error) {{
                    console.error('❌ Error showing success message:', error);
                }}
            }}
            
            // Initialize voices when available
            if ('speechSynthesis' in window) {{
                speechSynthesis.onvoiceschanged = function() {{
                    console.log('🗣️ Speech synthesis voices loaded');
                }};
            }}
            
            // Global error handler
            window.addEventListener('error', function(event) {{
                console.error('❌ Global error:', event.error);
                showErrorMessage('An unexpected error occurred');
            }});
            
            // Unhandled promise rejection handler
            window.addEventListener('unhandledrejection', function(event) {{
                console.error('❌ Unhandled promise rejection:', event.reason);
                showErrorMessage('An unexpected error occurred');
            }});
            
            console.log('🎉 Cyra Professional loaded successfully!');
        </script>
    </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    user_id = f"ws_user_{len(active_connections)}"
    active_connections[user_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            is_voice_call = message_data.get("is_voice_call", False)
            
            result = await ai_brain.process_message(
                message_data.get("message", ""),
                user_id,
                is_voice_call=is_voice_call
            )
            
            await websocket.send_text(json.dumps({
                "type": "response",
                "message": result["response"],
                "tool_calls": result.get("tool_calls", [])
            }))
            
    except WebSocketDisconnect:
        if user_id in active_connections:
            del active_connections[user_id]
        logger.info(f"WebSocket client {user_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if user_id in active_connections:
            del active_connections[user_id]

@app.post("/chat")
async def chat_endpoint(request: ChatMessage):
    """Process a chat message with Cyra"""
    try:
        result = await ai_brain.process_message(
            request.message, 
            request.user_id, 
            is_voice_call=request.is_voice_call
        )
        
        if request.conversation_id:
            if request.conversation_id not in conversations:
                conversations[request.conversation_id] = []
            
            conversations[request.conversation_id].extend([
                {"role": "user", "content": request.message, "timestamp": datetime.now().isoformat()},
                {"role": "assistant", "content": result["response"], "timestamp": datetime.now().isoformat()}
            ])
        
        return {
            "response": result["response"],
            "tool_calls": result.get("tool_calls", []),
            "conversation_id": result.get("conversation_id", 0),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {
            "ai_brain": ai_brain is not None,
            "tool_manager": tool_manager is not None,
            "websocket_connections": len(active_connections),
            "conversations": len(conversations)
        },
        "features": {
            "voice_recognition": True,
            "text_to_speech": True,
            "live_conversation": True,
            "real_time_chat": True,
            "icons8_integration": True,
            "error_handling": True
        },
        "timestamp": datetime.now(),
        "message": "Cyra AI Assistant Professional - All systems operational"
    }

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    favicon_path = "assets/icons/favicon.ico"
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    else:
        # Return a default favicon response
        return Response(status_code=204)

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "cyra_professional:app",
        host=settings.host,
        port=8005,
        reload=False,
        log_level=settings.log_level.lower()
    )
