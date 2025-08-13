"""
Cyra AI Assistant - Enhanced Live Chat with Voice Animations
===========================================================

Professional live chat with synchronized voice animations like Perplexity and ChatGPT
"""
import asyncio
import logging
import os
import json
import base64
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Response
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
    
    logger.info("🚀 Starting Cyra Enhanced Live Chat...")
    
    try:
        ai_brain = AIBrain()
        tool_manager = ToolManager()
        logger.info("✅ Enhanced services initialized")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize: {e}")
        raise
    
    yield
    logger.info("🛑 Shutting down Cyra Enhanced...")

# Create FastAPI app
app = FastAPI(
    title="Cyra Enhanced Live Chat",
    description="Professional live chat with voice animations",
    version="3.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("assets"):
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """Enhanced live chat interface with voice animations"""
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cyra Enhanced Live Chat</title>
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
            
            /* Enhanced Sidebar */
            .sidebar {{
                width: 280px;
                background: rgba(15, 15, 35, 0.98);
                backdrop-filter: blur(25px);
                border-right: 1px solid rgba(255, 255, 255, 0.12);
                display: flex;
                flex-direction: column;
                position: relative;
                z-index: 100;
                box-shadow: 4px 0 30px rgba(0, 0, 0, 0.4);
            }}
            
            .sidebar-header {{
                padding: 25px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.12);
            }}
            
            .logo {{
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 25px;
            }}
            
            .logo-icon {{
                width: 48px;
                height: 48px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: bold;
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
            }}
            
            .logo-text {{
                font-size: 28px;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .new-chat-btn {{
                width: 100%;
                padding: 14px 18px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                border-radius: 14px;
                color: white;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 10px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
            }}
            
            .new-chat-btn:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
            }}
            
            /* Enhanced Main Content */
            .main-content {{
                flex: 1;
                display: flex;
                flex-direction: column;
                position: relative;
                z-index: 10;
            }}
            
            .chat-header {{
                padding: 25px 35px;
                background: rgba(15, 15, 35, 0.98);
                backdrop-filter: blur(25px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.12);
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 4px 25px rgba(0, 0, 0, 0.15);
            }}
            
            .chat-title {{
                display: flex;
                align-items: center;
                gap: 15px;
                font-size: 22px;
                font-weight: 700;
            }}
            
            .title-icon {{
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
            }}
            
            .voice-controls {{
                display: flex;
                gap: 15px;
            }}
            
            .voice-btn {{
                padding: 12px 18px;
                border: none;
                border-radius: 12px;
                color: white;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 10px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
                min-width: 120px;
                justify-content: center;
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
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
            }}
            
            .voice-btn.speak {{
                background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
                box-shadow: 0 6px 20px rgba(6, 182, 212, 0.35);
            }}
            
            .voice-btn.live-call {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35);
            }}
            
            .voice-btn.recording {{
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                animation: pulse 1.5s infinite;
            }}
            
            .voice-btn.active {{
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                transform: scale(1.05);
                box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
            }}
            
            .voice-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            }}
            
            /* Enhanced Chat Messages */
            .chat-messages {{
                flex: 1;
                padding: 35px;
                overflow-y: auto;
                scroll-behavior: smooth;
            }}
            
            .message {{
                display: flex;
                gap: 18px;
                margin-bottom: 30px;
                animation: messageSlideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            .message.user {{
                flex-direction: row-reverse;
            }}
            
            .message-avatar {{
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                font-size: 18px;
                flex-shrink: 0;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
                position: relative;
            }}
            
            .message.user .message-avatar {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            
            .message.assistant .message-avatar {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            }}
            
            /* Voice Animation on Avatar */
            .message-avatar.speaking {{
                animation: voiceAnimation 0.8s ease-in-out infinite;
            }}
            
            .message-avatar.speaking::after {{
                content: '';
                position: absolute;
                inset: -8px;
                border-radius: 50%;
                background: linear-gradient(135deg, #10b981, #059669);
                opacity: 0.3;
                animation: voicePulse 1.2s ease-in-out infinite;
            }}
            
            @keyframes voiceAnimation {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
            }}
            
            @keyframes voicePulse {{
                0% {{ transform: scale(1); opacity: 0.6; }}
                100% {{ transform: scale(1.5); opacity: 0; }}
            }}
            
            .message-content {{
                flex: 1;
                max-width: 75%;
            }}
            
            .message.user .message-content {{
                text-align: right;
            }}
            
            .message-text {{
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(15px);
                padding: 18px 24px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.12);
                line-height: 1.7;
                margin-bottom: 10px;
                position: relative;
                box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
                transition: all 0.3s ease;
            }}
            
            .message-text:hover {{
                background: rgba(255, 255, 255, 0.12);
                transform: translateY(-2px);
            }}
            
            .message.user .message-text {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px 20px 6px 20px;
            }}
            
            .message.assistant .message-text {{
                background: rgba(255, 255, 255, 0.06);
                border-radius: 20px 20px 20px 6px;
            }}
            
            /* Enhanced Typing Indicator */
            .typing-indicator {{
                display: none;
                align-items: center;
                gap: 18px;
                margin-bottom: 30px;
                animation: messageSlideIn 0.4s ease-out;
            }}
            
            .typing-indicator.active {{
                display: flex;
            }}
            
            .typing-dots {{
                display: flex;
                gap: 6px;
                padding: 18px 24px;
                background: rgba(255, 255, 255, 0.06);
                border-radius: 20px 20px 20px 6px;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }}
            
            .typing-dot {{
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #10b981;
                animation: typingDots 1.6s infinite ease-in-out;
            }}
            
            .typing-dot:nth-child(2) {{ animation-delay: 0.3s; }}
            .typing-dot:nth-child(3) {{ animation-delay: 0.6s; }}
            
            @keyframes typingDots {{
                0%, 60%, 100% {{ transform: translateY(0); opacity: 0.4; }}
                30% {{ transform: translateY(-12px); opacity: 1; }}
            }}
            
            /* Enhanced Input Area */
            .input-area {{
                padding: 25px 35px 35px;
                background: rgba(15, 15, 35, 0.98);
                backdrop-filter: blur(25px);
                border-top: 1px solid rgba(255, 255, 255, 0.12);
            }}
            
            .input-container {{
                position: relative;
                max-width: 900px;
                margin: 0 auto;
            }}
            
            .message-input {{
                width: 100%;
                min-height: 60px;
                max-height: 160px;
                padding: 18px 70px 18px 24px;
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(15px);
                border: 2px solid rgba(255, 255, 255, 0.12);
                border-radius: 18px;
                color: #ffffff;
                font-size: 16px;
                font-family: inherit;
                resize: none;
                outline: none;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
            }}
            
            .message-input:focus {{
                border-color: rgba(102, 126, 234, 0.6);
                box-shadow: 0 8px 30px rgba(102, 126, 234, 0.25);
                background: rgba(255, 255, 255, 0.12);
            }}
            
            .message-input::placeholder {{
                color: rgba(255, 255, 255, 0.5);
            }}
            
            .send-btn {{
                position: absolute;
                right: 10px;
                top: 50%;
                transform: translateY(-50%);
                width: 50px;
                height: 50px;
                border: none;
                border-radius: 14px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35);
            }}
            
            .send-btn:hover:not(:disabled) {{
                transform: translateY(-50%) scale(1.08);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.45);
            }}
            
            .send-btn:disabled {{
                background: rgba(255, 255, 255, 0.1);
                cursor: not-allowed;
                box-shadow: none;
            }}
            
            /* Enhanced Voice Status */
            .voice-status {{
                position: fixed;
                bottom: 140px;
                right: 35px;
                background: rgba(15, 15, 35, 0.98);
                backdrop-filter: blur(25px);
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 18px;
                padding: 18px 24px;
                display: none;
                align-items: center;
                gap: 15px;
                box-shadow: 0 12px 45px rgba(0, 0, 0, 0.35);
                z-index: 1000;
                animation: voiceStatusSlide 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }}
            
            .voice-status.active {{
                display: flex;
            }}
            
            @keyframes voiceStatusSlide {{
                from {{ transform: translateX(100%) scale(0.8); opacity: 0; }}
                to {{ transform: translateX(0) scale(1); opacity: 1; }}
            }}
            
            .voice-indicator {{
                width: 14px;
                height: 14px;
                border-radius: 50%;
                background: #ef4444;
                animation: voiceIndicatorPulse 1.2s infinite;
                position: relative;
            }}
            
            .voice-indicator::after {{
                content: '';
                position: absolute;
                inset: -6px;
                border-radius: 50%;
                background: #ef4444;
                opacity: 0.3;
                animation: voiceIndicatorRing 2s infinite;
            }}
            
            @keyframes voiceIndicatorPulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.6; }}
            }}
            
            @keyframes voiceIndicatorRing {{
                0% {{ transform: scale(1); opacity: 0.6; }}
                100% {{ transform: scale(2); opacity: 0; }}
            }}
            
            .voice-text {{
                color: #ffffff;
                font-size: 15px;
                font-weight: 600;
            }}
            
            /* Live Chat Specific Animations */
            .live-chat-active .chat-messages {{
                background: radial-gradient(circle at center, rgba(16, 185, 129, 0.03) 0%, transparent 70%);
            }}
            
            .live-chat-pulse {{
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 200px;
                height: 200px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%);
                animation: liveChatPulse 2s infinite;
                pointer-events: none;
                z-index: 1;
            }}
            
            @keyframes liveChatPulse {{
                0% {{ transform: translate(-50%, -50%) scale(0.8); opacity: 0.8; }}
                100% {{ transform: translate(-50%, -50%) scale(1.5); opacity: 0; }}
            }}
            
            /* Enhanced Animations */
            @keyframes messageSlideIn {{
                from {{ 
                    opacity: 0; 
                    transform: translateY(20px) scale(0.95); 
                }}
                to {{ 
                    opacity: 1; 
                    transform: translateY(0) scale(1); 
                }}
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; transform: scale(1); }}
                50% {{ opacity: 0.8; transform: scale(1.05); }}
            }}
            
            /* Responsive Design */
            @media (max-width: 768px) {{
                .sidebar {{
                    width: 100%;
                    position: fixed;
                    left: 0;
                    top: 0;
                    z-index: 1000;
                    transform: translateX(-100%);
                    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }}
                
                .sidebar.open {{
                    transform: translateX(0);
                }}
                
                .main-content {{
                    width: 100%;
                }}
                
                .chat-header {{
                    padding: 20px 25px;
                }}
                
                .voice-controls {{
                    gap: 10px;
                }}
                
                .voice-btn {{
                    padding: 10px 14px;
                    font-size: 13px;
                    min-width: 100px;
                }}
                
                .chat-messages {{
                    padding: 25px;
                }}
                
                .message-content {{
                    max-width: 85%;
                }}
                
                .input-area {{
                    padding: 20px 25px 25px;
                }}
            }}
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {{
                width: 10px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: rgba(255, 255, 255, 0.05);
                border-radius: 6px;
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                transition: background 0.3s ease;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: rgba(255, 255, 255, 0.3);
            }}
        </style>
    </head>
    <body>
        <div class="app-container" id="appContainer">
            <!-- Live Chat Pulse Effect -->
            <div class="live-chat-pulse" id="liveChatPulse" style="display: none;"></div>
            
            <!-- Sidebar -->
            <div class="sidebar" id="sidebar">
                <div class="sidebar-header">
                    <div class="logo">
                        <div class="logo-icon">C</div>
                        <div class="logo-text">Cyra</div>
                    </div>
                    <button class="new-chat-btn" onclick="startNewChat()">
                        <i class="fas fa-plus"></i>
                        New Live Chat
                    </button>
                </div>
                
                <div class="conversations-list" id="conversationsList">
                    <div class="conversation-item active">
                        <i class="fas fa-comments"></i>
                        Enhanced Live Chat
                    </div>
                </div>
                
                <div class="sidebar-footer">
                    <div class="user-info">
                        <div class="user-avatar">U</div>
                        <div>
                            <div style="font-weight: 600;">Live Chat User</div>
                            <div style="font-size: 12px; color: rgba(255,255,255,0.6);">Premium Experience</div>
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
                        Cyra Enhanced Live Chat
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
                            <span>Live Chat</span>
                        </button>
                    </div>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message assistant">
                        <div class="message-avatar">C</div>
                        <div class="message-content">
                            <div class="message-text">
                                Hey there! 👋 I'm Cyra with enhanced live chat and perfect voice sync! 
                                <br><br>
                                ✨ <strong>New Features:</strong><br>
                                🎙️ <strong>Perfect Voice Sync</strong> - Like Perplexity & ChatGPT<br>
                                🎨 <strong>Live Animations</strong> - Real-time visual feedback<br>  
                                ⚡ <strong>Zero Delays</strong> - Instant responses<br>
                                📞 <strong>Enhanced Live Chat</strong> - Smooth conversations
                                <br><br>
                                Click <em>"Live Chat"</em> and start speaking! 🚀
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
                            placeholder="Message Cyra with enhanced live chat..." 
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
        
        <!-- Enhanced Voice Status -->
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
            let speechSynthesis = window.speechSynthesis;
            let currentUtterance = null;
            let audioContext = null;
            let audioAnalyser = null;
            let isProcessingVoice = false;
            
            // Initialize the application
            document.addEventListener('DOMContentLoaded', function() {{
                console.log('🚀 Initializing Cyra Enhanced Live Chat...');
                initializeSpeechRecognition();
                initializeWebSocket();
                initializeAudioContext();
                loadConversations();
                focusInput();
                console.log('✅ Enhanced live chat initialized successfully');
            }});
            
            // Initialize Audio Context for voice animations
            function initializeAudioContext() {{
                try {{
                    audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    audioAnalyser = audioContext.createAnalyser();
                    audioAnalyser.fftSize = 256;
                    console.log('✅ Audio context initialized for voice animations');
                }} catch (error) {{
                    console.warn('⚠️ Audio context not available');
                }}
            }}
            
            // Enhanced WebSocket with instant response
            function initializeWebSocket() {{
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${{protocol}}//${{window.location.host}}/ws`;
                
                try {{
                    websocket = new WebSocket(wsUrl);
                    
                    websocket.onopen = function() {{
                        console.log('✅ Enhanced WebSocket connected');
                        showSuccessMessage('🚀 Live chat ready!');
                    }};
                    
                    websocket.onmessage = function(event) {{
                        try {{
                            const data = JSON.parse(event.data);
                            if (data.type === 'response') {{
                                // Instant response - no delays
                                hideTypingIndicator();
                                addMessage('assistant', data.message);
                                
                                // Enhanced voice response with animations
                                if (isSpeechEnabled || isLiveCallActive) {{
                                    speakTextWithAnimation(data.message);
                                }}
                            }}
                        }} catch (error) {{
                            console.error('❌ WebSocket message error:', error);
                        }}
                    }};
                    
                    websocket.onclose = function() {{
                        console.log('🔄 WebSocket reconnecting...');
                        setTimeout(initializeWebSocket, 1000); // Faster reconnection
                    }};
                    
                    websocket.onerror = function(error) {{
                        console.error('❌ WebSocket error:', error);
                    }};
                    
                }} catch (error) {{
                    console.warn('⚠️ WebSocket fallback to HTTP');
                }}
            }}
            
            // Enhanced Speech Recognition
            function initializeSpeechRecognition() {{
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    recognition = new SpeechRecognition();
                    recognition.continuous = true;
                    recognition.interimResults = true;
                    recognition.lang = 'en-US';
                    recognition.maxAlternatives = 1;
                    
                    recognition.onstart = function() {{
                        console.log('🎤 Enhanced speech recognition started');
                        isProcessingVoice = false;
                    }};
                    
                    recognition.onresult = function(event) {{
                        if (isProcessingVoice) return; // Prevent multiple processing
                        
                        let finalTranscript = '';
                        let interimTranscript = '';
                        
                        for (let i = event.resultIndex; i < event.results.length; ++i) {{
                            if (event.results[i].isFinal) {{
                                finalTranscript += event.results[i][0].transcript;
                            }} else {{
                                interimTranscript += event.results[i][0].transcript;
                            }}
                        }}
                        
                        // Update input with interim results for live feedback
                        const input = document.getElementById('messageInput');
                        if (interimTranscript) {{
                            input.placeholder = `Listening: "${{interimTranscript}}"...`;
                        }}
                        
                        if (finalTranscript) {{
                            isProcessingVoice = true;
                            input.value = finalTranscript.trim();
                            input.placeholder = "Message Cyra with enhanced live chat...";
                            autoResize(input);
                            
                            if (isLiveCallActive) {{
                                // Instant send in live chat mode
                                setTimeout(() => {{
                                    sendMessage();
                                    isProcessingVoice = false;
                                }}, 100);
                            }} else {{
                                isProcessingVoice = false;
                            }}
                        }}
                    }};
                    
                    recognition.onerror = function(event) {{
                        console.error('❌ Speech recognition error:', event.error);
                        isProcessingVoice = false;
                        if (event.error !== 'no-speech') {{
                            showErrorMessage('Speech recognition error: ' + event.error);
                        }}
                    }};
                    
                    recognition.onend = function() {{
                        if ((isRecording || isLiveCallActive) && !isProcessingVoice) {{
                            try {{
                                recognition.start();
                            }} catch (error) {{
                                console.error('❌ Error restarting recognition:', error);
                            }}
                        }}
                    }};
                    
                    console.log('✅ Enhanced speech recognition initialized');
                }} else {{
                    console.warn('⚠️ Speech recognition not supported');
                    showErrorMessage('Speech recognition not supported in this browser');
                }}
            }}
            
            // Enhanced Voice Recording
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
                    
                    showVoiceStatus('🎤 Recording with enhanced feedback...');
                    recognition.start();
                    console.log('🎤 Enhanced recording started');
                }} catch (error) {{
                    console.error('❌ Recording error:', error);
                    showErrorMessage('Failed to start recording');
                    isRecording = false;
                }}
            }}
            
            function stopRecording() {{
                try {{
                    isRecording = false;
                    isProcessingVoice = false;
                    const recordBtn = document.getElementById('recordBtn');
                    recordBtn.classList.remove('recording');
                    recordBtn.innerHTML = '<i class="fas fa-microphone"></i><span>Record</span>';
                    
                    hideVoiceStatus();
                    if (recognition) {{
                        recognition.stop();
                    }}
                    
                    // Reset placeholder
                    document.getElementById('messageInput').placeholder = "Message Cyra with enhanced live chat...";
                    console.log('🎤 Recording stopped');
                }} catch (error) {{
                    console.error('❌ Error stopping recording:', error);
                }}
            }}
            
            // Enhanced Speech Synthesis with Animations
            function toggleSpeech() {{
                isSpeechEnabled = !isSpeechEnabled;
                const speakBtn = document.getElementById('speakBtn');
                
                if (isSpeechEnabled) {{
                    speakBtn.classList.add('active');
                    speakBtn.innerHTML = '<i class="fas fa-volume-mute"></i><span>Mute</span>';
                    console.log('🔊 Enhanced speech enabled');
                }} else {{
                    speakBtn.classList.remove('active');
                    speakBtn.innerHTML = '<i class="fas fa-volume-up"></i><span>Speech</span>';
                    speechSynthesis.cancel();
                    stopVoiceAnimation();
                    console.log('🔇 Speech disabled');
                }}
            }}
            
            function speakTextWithAnimation(text) {{
                if (!isSpeechEnabled && !isLiveCallActive) return;
                if (!('speechSynthesis' in window)) {{
                    console.warn('⚠️ Speech synthesis not supported');
                    return;
                }}
                
                try {{
                    // Stop any ongoing speech
                    speechSynthesis.cancel();
                    stopVoiceAnimation();
                    
                    // Clean text for speech
                    const cleanText = text
                        .replace(/\\*\\*(.*?)\\*\\*/g, '$1')
                        .replace(/\\*(.*?)\\*/g, '$1')
                        .replace(/<[^>]*>/g, '')
                        .replace(/🔐|🛡️|🎤|📞|😊|👋|✨|🎙️|🎨|⚡|🚀/g, '');
                    
                    currentUtterance = new SpeechSynthesisUtterance(cleanText);
                    currentUtterance.rate = 1.0; // Faster rate for better sync
                    currentUtterance.pitch = 1.1;
                    currentUtterance.volume = 0.9;
                    
                    // Get female voice
                    const voices = speechSynthesis.getVoices();
                    const femaleVoice = voices.find(voice => 
                        voice.name.includes('Female') || 
                        voice.name.includes('Zira') || 
                        voice.name.includes('Aria') ||
                        voice.name.includes('Samantha') ||
                        voice.gender === 'female'
                    );
                    
                    if (femaleVoice) {{
                        currentUtterance.voice = femaleVoice;
                    }}
                    
                    currentUtterance.onstart = function() {{
                        console.log('🗣️ Enhanced speech started with animation');
                        startVoiceAnimation();
                    }};
                    
                    currentUtterance.onend = function() {{
                        console.log('🗣️ Speech ended');
                        stopVoiceAnimation();
                    }};
                    
                    currentUtterance.onerror = function(event) {{
                        console.error('❌ Speech synthesis error:', event.error);
                        stopVoiceAnimation();
                    }};
                    
                    // Start speaking immediately - no delays
                    speechSynthesis.speak(currentUtterance);
                    
                }} catch (error) {{
                    console.error('❌ Error in enhanced speech synthesis:', error);
                    stopVoiceAnimation();
                }}
            }}
            
            // Voice Animation Functions (like Perplexity/ChatGPT)
            function startVoiceAnimation() {{
                const assistantAvatars = document.querySelectorAll('.message.assistant .message-avatar');
                assistantAvatars.forEach(avatar => {{
                    avatar.classList.add('speaking');
                }});
                
                // Add live chat visual effects
                if (isLiveCallActive) {{
                    document.getElementById('appContainer').classList.add('live-chat-active');
                    document.getElementById('liveChatPulse').style.display = 'block';
                }}
            }}
            
            function stopVoiceAnimation() {{
                const assistantAvatars = document.querySelectorAll('.message.assistant .message-avatar');
                assistantAvatars.forEach(avatar => {{
                    avatar.classList.remove('speaking');
                }});
                
                // Remove live chat visual effects
                document.getElementById('appContainer').classList.remove('live-chat-active');
                document.getElementById('liveChatPulse').style.display = 'none';
            }}
            
            // Enhanced Live Call Functions
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
                    liveCallBtn.innerHTML = '<i class="fas fa-phone-slash"></i><span>End Chat</span>';
                    
                    const speakBtn = document.getElementById('speakBtn');
                    speakBtn.classList.add('active');
                    speakBtn.innerHTML = '<i class="fas fa-volume-mute"></i><span>Mute</span>';
                    
                    showVoiceStatus('📞 Enhanced live chat active - Speak naturally');
                    
                    // Add live chat visual effects
                    document.getElementById('appContainer').classList.add('live-chat-active');
                    
                    recognition.start();
                    
                    addMessage('system', '📞 Enhanced live chat started! Speak naturally with perfect voice sync.');
                    console.log('📞 Enhanced live chat started');
                }} catch (error) {{
                    console.error('❌ Error starting live chat:', error);
                    showErrorMessage('Failed to start live chat');
                    isLiveCallActive = false;
                }}
            }}
            
            function stopLiveCall() {{
                try {{
                    isLiveCallActive = false;
                    isProcessingVoice = false;
                    
                    const liveCallBtn = document.getElementById('liveCallBtn');
                    liveCallBtn.classList.remove('active');
                    liveCallBtn.innerHTML = '<i class="fas fa-phone"></i><span>Live Chat</span>';
                    
                    hideVoiceStatus();
                    stopVoiceAnimation();
                    
                    // Remove live chat visual effects
                    document.getElementById('appContainer').classList.remove('live-chat-active');
                    document.getElementById('liveChatPulse').style.display = 'none';
                    
                    if (recognition) {{
                        recognition.stop();
                    }}
                    
                    if (speechSynthesis) {{
                        speechSynthesis.cancel();
                    }}
                    
                    // Reset input placeholder
                    document.getElementById('messageInput').placeholder = "Message Cyra with enhanced live chat...";
                    
                    addMessage('system', '📞 Enhanced live chat ended.');
                    console.log('📞 Live chat ended');
                }} catch (error) {{
                    console.error('❌ Error stopping live chat:', error);
                }}
            }}
            
            // Enhanced Voice Status Functions
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
            
            // Enhanced Message Functions
            async function sendMessage() {{
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                try {{
                    // Add user message with animation
                    addMessage('user', message);
                    input.value = '';
                    autoResize(input);
                    
                    // Show enhanced typing indicator
                    showTypingIndicator();
                    
                    // Send with instant processing
                    const response = await fetch('/chat', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ 
                            message, 
                            user_id: 'enhanced_user',
                            conversation_id: currentConversationId,
                            is_voice_call: isLiveCallActive
                        }})
                    }});
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    
                    const data = await response.json();
                    
                    // Instant response processing
                    hideTypingIndicator();
                    addMessage('assistant', data.response);
                    
                    // Handle tool calls
                    if (data.tool_calls && data.tool_calls.length > 0) {{
                        data.tool_calls.forEach(tool => {{
                            if (tool.result && tool.result.result) {{
                                displayToolResult(tool);
                            }}
                        }});
                    }}
                    
                    // Enhanced voice response
                    if (isSpeechEnabled || isLiveCallActive) {{
                        speakTextWithAnimation(data.response);
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
                            <div style="text-align: center; color: rgba(255,255,255,0.8); font-style: italic; margin: 15px 0; padding: 12px; background: rgba(16, 185, 129, 0.1); border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.2);">
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
                    content = content.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
                    content = content.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
                    content = content.replace(/`(.*?)`/g, '<code>$1</code>');
                    content = content.replace(/\\n/g, '<br>');
                    return content;
                }} catch (error) {{
                    console.error('❌ Error formatting message:', error);
                    return content;
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
                    const indicator = document.getElementById('typingIndicator');
                    indicator.classList.add('active');
                    const messagesContainer = document.getElementById('chatMessages');
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                }} catch (error) {{
                    console.error('❌ Error showing typing indicator:', error);
                }}
            }}
            
            function hideTypingIndicator() {{
                try {{
                    const indicator = document.getElementById('typingIndicator');
                    indicator.classList.remove('active');
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
                    textarea.style.height = Math.min(textarea.scrollHeight, 160) + 'px';
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
                    
                    addMessage('assistant', `Hey there! 👋 I'm Cyra with enhanced live chat and perfect voice sync! 

✨ **New Features:**
🎙️ **Perfect Voice Sync** - Like Perplexity & ChatGPT
🎨 **Live Animations** - Real-time visual feedback  
⚡ **Zero Delays** - Instant responses
📞 **Enhanced Live Chat** - Smooth conversations

Click *"Live Chat"* and start speaking! 🚀`);
                    
                    focusInput();
                    console.log('🆕 New enhanced chat started');
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
                            Enhanced Live Chat
                        </div>
                    `;
                }} catch (error) {{
                    console.error('❌ Error loading conversations:', error);
                }}
            }}
            
            // Enhanced Error and Success Messages
            function showErrorMessage(message) {{
                try {{
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error-message';
                    errorDiv.style.cssText = `
                        background: rgba(239, 68, 68, 0.15);
                        border: 1px solid rgba(239, 68, 68, 0.4);
                        color: #fca5a5;
                        padding: 12px 16px;
                        border-radius: 12px;
                        margin: 10px 0;
                        animation: messageSlideIn 0.3s ease-out;
                    `;
                    errorDiv.textContent = message;
                    
                    const messagesContainer = document.getElementById('chatMessages');
                    messagesContainer.appendChild(errorDiv);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    
                    setTimeout(() => {{
                        if (errorDiv.parentNode) {{
                            errorDiv.style.animation = 'messageSlideIn 0.3s ease-out reverse';
                            setTimeout(() => errorDiv.remove(), 300);
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
                    successDiv.style.cssText = `
                        background: rgba(16, 185, 129, 0.15);
                        border: 1px solid rgba(16, 185, 129, 0.4);
                        color: #6ee7b7;
                        padding: 12px 16px;
                        border-radius: 12px;
                        margin: 10px 0;
                        animation: messageSlideIn 0.3s ease-out;
                    `;
                    successDiv.textContent = message;
                    
                    const messagesContainer = document.getElementById('chatMessages');
                    messagesContainer.appendChild(successDiv);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    
                    setTimeout(() => {{
                        if (successDiv.parentNode) {{
                            successDiv.style.animation = 'messageSlideIn 0.3s ease-out reverse';
                            setTimeout(() => successDiv.remove(), 300);
                        }}
                    }}, 3000);
                }} catch (error) {{
                    console.error('❌ Error showing success message:', error);
                }}
            }}
            
            // Initialize voices and audio
            if ('speechSynthesis' in window) {{
                speechSynthesis.onvoiceschanged = function() {{
                    console.log('🗣️ Enhanced speech synthesis voices loaded');
                }};
            }}
            
            // Global error handlers
            window.addEventListener('error', function(event) {{
                console.error('❌ Global error:', event.error);
                showErrorMessage('An unexpected error occurred');
            }});
            
            window.addEventListener('unhandledrejection', function(event) {{
                console.error('❌ Unhandled promise rejection:', event.reason);
                showErrorMessage('An unexpected error occurred');
            }});
            
            console.log('🎉 Cyra Enhanced Live Chat loaded successfully!');
        </script>
    </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Enhanced WebSocket with instant responses"""
    await websocket.accept()
    user_id = f"enhanced_user_{len(active_connections)}"
    active_connections[user_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            is_voice_call = message_data.get("is_voice_call", False)
            
            # Instant AI processing
            result = await ai_brain.process_message(
                message_data.get("message", ""),
                user_id,
                is_voice_call=is_voice_call
            )
            
            # Instant response - no delays
            await websocket.send_text(json.dumps({
                "type": "response",
                "message": result["response"],
                "tool_calls": result.get("tool_calls", [])
            }))
            
    except WebSocketDisconnect:
        if user_id in active_connections:
            del active_connections[user_id]
        logger.info(f"Enhanced user {user_id} disconnected")
    except Exception as e:
        logger.error(f"Enhanced WebSocket error: {e}")
        if user_id in active_connections:
            del active_connections[user_id]

@app.post("/chat")
async def chat_endpoint(request: ChatMessage):
    """Enhanced chat endpoint with instant processing"""
    try:
        # Instant AI processing - no delays
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
        logger.error(f"Enhanced chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Enhanced health check"""
    return {
        "status": "enhanced",
        "version": "3.0.0",
        "services": {
            "ai_brain": ai_brain is not None,
            "tool_manager": tool_manager is not None,
            "websocket_connections": len(active_connections),
            "conversations": len(conversations)
        },
        "features": {
            "voice_sync_animations": True,
            "zero_delay_responses": True,
            "live_chat_enhanced": True,
            "perplexity_style_animations": True,
            "instant_processing": True
        },
        "timestamp": datetime.now(),
        "message": "Cyra Enhanced Live Chat - Perfect Voice Sync Ready"
    }

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    favicon_path = "assets/icons/favicon.ico"
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    else:
        return Response(status_code=204)

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "cyra_enhanced:app",
        host=settings.host,
        port=8007,
        reload=False,
        log_level=settings.log_level.lower()
    )
