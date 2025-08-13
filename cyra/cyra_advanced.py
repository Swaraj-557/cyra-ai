"""
Cyra AI Assistant - Advanced Web Application with Voice Features
Modern ChatGPT-like interface with voice recognition and live conversation
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
    is_voice_call: bool = False  # Flag for voice call mode

class VoiceMessage(BaseModel):
    audio_data: str  # Base64 encoded audio
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
    description="Advanced AI-powered cybersecurity assistant with voice capabilities",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static files directory for assets
import os
os.makedirs("static", exist_ok=True)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the modern ChatGPT-like interface"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cyra AI Assistant</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: #0f0f23;
                color: #ffffff;
                height: 100vh;
                overflow: hidden;
            }
            
            .app-container {
                display: flex;
                height: 100vh;
            }
            
            /* Sidebar */
            .sidebar {
                width: 260px;
                background: #202123;
                border-right: 1px solid #4d4d4f;
                display: flex;
                flex-direction: column;
                transition: transform 0.3s ease;
            }
            
            .sidebar-header {
                padding: 20px;
                border-bottom: 1px solid #4d4d4f;
            }
            
            .new-chat-btn {
                width: 100%;
                padding: 12px;
                background: transparent;
                border: 1px solid #4d4d4f;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 10px;
                transition: background 0.2s;
            }
            
            .new-chat-btn:hover {
                background: #40414f;
            }
            
            .conversations-list {
                flex: 1;
                overflow-y: auto;
                padding: 10px;
            }
            
            .conversation-item {
                padding: 12px;
                margin: 4px 0;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                color: #ececf1;
                transition: background 0.2s;
                position: relative;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            .conversation-item:hover {
                background: #2a2b32;
            }
            
            .conversation-item.active {
                background: #40414f;
            }
            
            .sidebar-footer {
                padding: 20px;
                border-top: 1px solid #4d4d4f;
            }
            
            .user-info {
                display: flex;
                align-items: center;
                gap: 10px;
                color: #ececf1;
                font-size: 14px;
            }
            
            .user-avatar {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea, #764ba2);
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
            }
            
            /* Main Chat Area */
            .main-content {
                flex: 1;
                display: flex;
                flex-direction: column;
                background: #343541;
            }
            
            .chat-header {
                padding: 15px 20px;
                border-bottom: 1px solid #4d4d4f;
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: #40414f;
            }
            
            .chat-title {
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
            }
            
            .voice-controls {
                display: flex;
                gap: 10px;
            }
            
            .voice-btn {
                padding: 8px 12px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 6px;
            }
            
            .voice-btn.record {
                background: #10a37f;
                color: white;
            }
            
            .voice-btn.record:hover {
                background: #0d8a68;
            }
            
            .voice-btn.record.recording {
                background: #ef4444;
                animation: pulse 1s infinite;
            }
            
            .voice-btn.speak {
                background: #6366f1;
                color: white;
            }
            
            .voice-btn.speak:hover {
                background: #4f46e5;
            }
            
            .voice-btn.live-call {
                background: #f59e0b;
                color: white;
            }
            
            .voice-btn.live-call:hover {
                background: #d97706;
            }
            
            .voice-btn.live-call.active {
                background: #ef4444;
                animation: pulse 1s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            
            .message {
                display: flex;
                gap: 15px;
                max-width: 100%;
                animation: fadeIn 0.3s ease-in;
            }
            
            .message.user {
                flex-direction: row-reverse;
            }
            
            .message-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                flex-shrink: 0;
                font-size: 16px;
            }
            
            .message.user .message-avatar {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
            }
            
            .message.assistant .message-avatar {
                background: #10a37f;
                color: white;
            }
            
            .message-content {
                flex: 1;
                background: #444654;
                padding: 15px 20px;
                border-radius: 12px;
                position: relative;
                max-width: 70%;
            }
            
            .message.user .message-content {
                background: #40414f;
                text-align: right;
            }
            
            .message-text {
                line-height: 1.6;
                color: #ececf1;
            }
            
            .message-time {
                font-size: 12px;
                color: #8e8ea0;
                margin-top: 8px;
            }
            
            .typing-indicator {
                display: none;
                align-items: center;
                gap: 15px;
                opacity: 0.7;
            }
            
            .typing-dots {
                display: flex;
                gap: 4px;
            }
            
            .typing-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #10a37f;
                animation: typing 1.4s infinite ease-in-out;
            }
            
            .typing-dot:nth-child(1) { animation-delay: -0.32s; }
            .typing-dot:nth-child(2) { animation-delay: -0.16s; }
            
            @keyframes typing {
                0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
                40% { transform: scale(1); opacity: 1; }
            }
            
            /* Input Area */
            .input-area {
                padding: 20px;
                border-top: 1px solid #4d4d4f;
                background: #40414f;
            }
            
            .input-container {
                position: relative;
                max-width: 800px;
                margin: 0 auto;
            }
            
            .message-input {
                width: 100%;
                min-height: 50px;
                max-height: 150px;
                padding: 15px 60px 15px 20px;
                background: #343541;
                border: 1px solid #4d4d4f;
                border-radius: 12px;
                color: #ffffff;
                font-size: 16px;
                font-family: inherit;
                resize: none;
                outline: none;
                transition: border-color 0.2s;
            }
            
            .message-input:focus {
                border-color: #10a37f;
            }
            
            .message-input::placeholder {
                color: #8e8ea0;
            }
            
            .send-btn {
                position: absolute;
                right: 10px;
                top: 50%;
                transform: translateY(-50%);
                width: 40px;
                height: 40px;
                border: none;
                border-radius: 8px;
                background: #10a37f;
                color: white;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background 0.2s;
            }
            
            .send-btn:hover:not(:disabled) {
                background: #0d8a68;
            }
            
            .send-btn:disabled {
                background: #4d4d4f;
                cursor: not-allowed;
            }
            
            /* Voice Status */
            .voice-status {
                position: fixed;
                bottom: 100px;
                right: 20px;
                background: #202123;
                border: 1px solid #4d4d4f;
                border-radius: 12px;
                padding: 15px;
                display: none;
                align-items: center;
                gap: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                z-index: 1000;
            }
            
            .voice-status.active {
                display: flex;
            }
            
            .voice-indicator {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #ef4444;
                animation: pulse 1s infinite;
            }
            
            .voice-text {
                color: #ececf1;
                font-size: 14px;
            }
            
            /* Mobile Responsive */
            @media (max-width: 768px) {
                .sidebar {
                    width: 100%;
                    position: fixed;
                    left: 0;
                    top: 0;
                    z-index: 1000;
                    transform: translateX(-100%);
                }
                
                .sidebar.open {
                    transform: translateX(0);
                }
                
                .main-content {
                    width: 100%;
                }
                
                .message-content {
                    max-width: 85%;
                }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* Code highlighting */
            pre {
                background: #2d2d2d;
                border-radius: 8px;
                padding: 15px;
                overflow-x: auto;
                margin: 10px 0;
            }
            
            code {
                background: #2d2d2d;
                padding: 2px 6px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
            }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #202123;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #4d4d4f;
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #666;
            }
        </style>
    </head>
    <body>
        <div class="app-container">
            <!-- Sidebar -->
            <div class="sidebar" id="sidebar">
                <div class="sidebar-header">
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
                            <div>Cybersecurity User</div>
                            <div style="font-size: 12px; color: #8e8ea0;">Premium Plan</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Main Content -->
            <div class="main-content">
                <div class="chat-header">
                    <div class="chat-title">
                        <i class="fas fa-shield-alt"></i>
                        Cyra AI Assistant
                    </div>
                    <div class="voice-controls">
                        <button class="voice-btn record" id="recordBtn" onclick="toggleRecording()">
                            <i class="fas fa-microphone"></i>
                            Record
                        </button>
                        <button class="voice-btn speak" id="speakBtn" onclick="toggleSpeech()">
                            <i class="fas fa-volume-up"></i>
                            Speech
                        </button>
                        <button class="voice-btn live-call" id="liveCallBtn" onclick="toggleLiveCall()">
                            <i class="fas fa-phone"></i>
                            Live Call
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
                                � <strong>Passwords</strong> - Generate & check them<br>
                                �️ <strong>Security Tips</strong> - Stay safe online<br>  
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
                    <div class="message-avatar" style="background: #10a37f; color: white;">C</div>
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
            document.addEventListener('DOMContentLoaded', function() {
                initializeSpeechRecognition();
                initializeWebSocket();
                loadConversations();
                focusInput();
            });
            
            // WebSocket connection for real-time communication
            function initializeWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws`;
                
                try {
                    websocket = new WebSocket(wsUrl);
                    
                    websocket.onopen = function() {
                        console.log('WebSocket connected');
                    };
                    
                    websocket.onmessage = function(event) {
                        const data = JSON.parse(event.data);
                        if (data.type === 'response') {
                            addMessage('assistant', data.message);
                            if (isSpeechEnabled) {
                                speakText(data.message);
                            }
                        }
                    };
                    
                    websocket.onclose = function() {
                        console.log('WebSocket disconnected');
                        // Attempt to reconnect after 3 seconds
                        setTimeout(initializeWebSocket, 3000);
                    };
                } catch (error) {
                    console.log('WebSocket not available, using HTTP fallback');
                }
            }
            
            // Speech Recognition Setup
            function initializeSpeechRecognition() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    recognition = new SpeechRecognition();
                    recognition.continuous = true;
                    recognition.interimResults = true;
                    recognition.lang = 'en-US';
                    
                    recognition.onresult = function(event) {
                        let finalTranscript = '';
                        let interimTranscript = '';
                        
                        for (let i = event.resultIndex; i < event.results.length; ++i) {
                            if (event.results[i].isFinal) {
                                finalTranscript += event.results[i][0].transcript;
                            } else {
                                interimTranscript += event.results[i][0].transcript;
                            }
                        }
                        
                        if (finalTranscript) {
                            document.getElementById('messageInput').value = finalTranscript;
                            if (isLiveCallActive) {
                                sendMessage();
                            }
                        }
                    };
                    
                    recognition.onerror = function(event) {
                        console.error('Speech recognition error:', event.error);
                        stopRecording();
                    };
                    
                    recognition.onend = function() {
                        if (isRecording || isLiveCallActive) {
                            recognition.start(); // Restart for continuous listening
                        }
                    };
                } else {
                    console.log('Speech recognition not supported');
                }
            }
            
            // Voice Recording Functions
            function toggleRecording() {
                if (isRecording) {
                    stopRecording();
                } else {
                    startRecording();
                }
            }
            
            function startRecording() {
                if (!recognition) {
                    alert('Speech recognition not supported in this browser');
                    return;
                }
                
                isRecording = true;
                const recordBtn = document.getElementById('recordBtn');
                recordBtn.classList.add('recording');
                recordBtn.innerHTML = '<i class="fas fa-stop"></i> Stop';
                
                showVoiceStatus('Listening...');
                recognition.start();
            }
            
            function stopRecording() {
                if (!recognition) return;
                
                isRecording = false;
                const recordBtn = document.getElementById('recordBtn');
                recordBtn.classList.remove('recording');
                recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Record';
                
                hideVoiceStatus();
                recognition.stop();
            }
            
            // Speech Synthesis Functions
            function toggleSpeech() {
                isSpeechEnabled = !isSpeechEnabled;
                const speakBtn = document.getElementById('speakBtn');
                
                if (isSpeechEnabled) {
                    speakBtn.style.background = '#ef4444';
                    speakBtn.innerHTML = '<i class="fas fa-volume-mute"></i> Mute';
                } else {
                    speakBtn.style.background = '#6366f1';
                    speakBtn.innerHTML = '<i class="fas fa-volume-up"></i> Speech';
                }
            }
            
            function speakText(text) {
                if (!isSpeechEnabled || !('speechSynthesis' in window)) return;
                
                // Stop any ongoing speech
                speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.9;
                utterance.pitch = 1.1;
                utterance.volume = 0.8;
                
                // Try to use a female voice
                const voices = speechSynthesis.getVoices();
                const femaleVoice = voices.find(voice => 
                    voice.name.includes('Female') || 
                    voice.name.includes('Zira') || 
                    voice.name.includes('Aria') ||
                    voice.gender === 'female'
                );
                
                if (femaleVoice) {
                    utterance.voice = femaleVoice;
                }
                
                speechSynthesis.speak(utterance);
            }
            
            // Live Call Functions
            function toggleLiveCall() {
                if (isLiveCallActive) {
                    stopLiveCall();
                } else {
                    startLiveCall();
                }
            }
            
            function startLiveCall() {
                if (!recognition) {
                    alert('Speech recognition not supported in this browser');
                    return;
                }
                
                isLiveCallActive = true;
                isSpeechEnabled = true;
                
                const liveCallBtn = document.getElementById('liveCallBtn');
                liveCallBtn.classList.add('active');
                liveCallBtn.innerHTML = '<i class="fas fa-phone-slash"></i> End Call';
                
                const speakBtn = document.getElementById('speakBtn');
                speakBtn.style.background = '#ef4444';
                speakBtn.innerHTML = '<i class="fas fa-volume-mute"></i> Mute';
                
                showVoiceStatus('Live call active - Speak naturally');
                recognition.start();
                
                // Add system message
                addMessage('system', '📞 Live call started. Speak naturally to Cyra.');
            }
            
            function stopLiveCall() {
                isLiveCallActive = false;
                
                const liveCallBtn = document.getElementById('liveCallBtn');
                liveCallBtn.classList.remove('active');
                liveCallBtn.innerHTML = '<i class="fas fa-phone"></i> Live Call';
                
                hideVoiceStatus();
                if (recognition) {
                    recognition.stop();
                }
                
                // Add system message
                addMessage('system', '📞 Live call ended.');
            }
            
            // Voice Status Functions
            function showVoiceStatus(text) {
                const voiceStatus = document.getElementById('voiceStatus');
                const voiceStatusText = document.getElementById('voiceStatusText');
                voiceStatusText.textContent = text;
                voiceStatus.classList.add('active');
            }
            
            function hideVoiceStatus() {
                const voiceStatus = document.getElementById('voiceStatus');
                voiceStatus.classList.remove('active');
            }
            
            // Message Functions
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Add user message
                addMessage('user', message);
                input.value = '';
                autoResize(input);
                
                // Show typing indicator
                showTypingIndicator();
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            message, 
                            user_id: 'web_user',
                            conversation_id: currentConversationId,
                            is_voice_call: isLiveCallActive  // Pass voice call status
                        })
                    });
                    
                    const data = await response.json();
                    
                    // Hide typing indicator
                    hideTypingIndicator();
                    
                    // Add assistant response
                    addMessage('assistant', data.response);
                    
                    // Handle tool calls
                    if (data.tool_calls && data.tool_calls.length > 0) {
                        data.tool_calls.forEach(tool => {
                            if (tool.result && tool.result.result) {
                                displayToolResult(tool);
                            }
                        });
                    }
                    
                    // Speak response if enabled
                    if (isSpeechEnabled || isLiveCallActive) {
                        speakText(data.response);
                    }
                    
                } catch (error) {
                    hideTypingIndicator();
                    addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
                    console.error('Error:', error);
                }
                
                focusInput();
            }
            
            function addMessage(sender, content, isSystem = false) {
                const messagesContainer = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                
                if (isSystem || sender === 'system') {
                    messageDiv.className = 'message system';
                    messageDiv.innerHTML = `
                        <div style="text-align: center; color: #8e8ea0; font-style: italic; margin: 10px 0;">
                            ${content}
                        </div>
                    `;
                } else {
                    messageDiv.className = `message ${sender}`;
                    const avatar = sender === 'user' ? 'U' : 'C';
                    const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                    
                    messageDiv.innerHTML = `
                        <div class="message-avatar">${avatar}</div>
                        <div class="message-content">
                            <div class="message-text">${formatMessage(content)}</div>
                            <div class="message-time">${time}</div>
                        </div>
                    `;
                }
                
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            function formatMessage(content) {
                // Basic markdown-like formatting
                content = content.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
                content = content.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
                content = content.replace(/`(.*?)`/g, '<code>$1</code>');
                content = content.replace(/\\n/g, '<br>');
                return content;
            }
            
            function displayToolResult(tool) {
                const result = tool.result.result;
                let message = '';
                
                if (result.password) {
                    message = `🔧 Generated password: <code>${result.password}</code><br>Strength: ${result.strength.level} (${result.strength.score}/100)`;
                } else if (result.passwords) {
                    message = '🔧 Generated passwords:<br>';
                    result.passwords.forEach(p => {
                        message += `<code>${p.password}</code> (${p.strength_level})<br>`;
                    });
                } else if (result.score !== undefined) {
                    message = `🔍 Password analysis: ${result.level} (${result.score}/100)<br>Estimated crack time: ${result.estimated_crack_time}`;
                }
                
                if (message) {
                    addMessage('assistant', message);
                }
            }
            
            function showTypingIndicator() {
                document.getElementById('typingIndicator').style.display = 'flex';
                const messagesContainer = document.getElementById('chatMessages');
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            function hideTypingIndicator() {
                document.getElementById('typingIndicator').style.display = 'none';
            }
            
            // Input Handling
            function handleKeyDown(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    sendMessage();
                }
            }
            
            function autoResize(textarea) {
                textarea.style.height = 'auto';
                textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
            }
            
            function focusInput() {
                document.getElementById('messageInput').focus();
            }
            
            // Conversation Management
            function startNewChat() {
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
            }
            
            function loadConversations() {
                // Placeholder for conversation history
                const conversationsList = document.getElementById('conversationsList');
                conversationsList.innerHTML = `
                    <div class="conversation-item active">
                        <i class="fas fa-comments" style="margin-right: 8px;"></i>
                        New Conversation
                    </div>
                `;
            }
            
            // Initialize voices when available
            if ('speechSynthesis' in window) {
                speechSynthesis.onvoiceschanged = function() {
                    // Voices are now loaded
                };
            }
        </script>
    </body>
    </html>
    """

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
            
            # Check if this is a voice call mode message
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

@app.post("/chat")
async def chat_endpoint(request: ChatMessage):
    """Process a chat message with Cyra"""
    try:
        result = await ai_brain.process_message(
            request.message, 
            request.user_id, 
            is_voice_call=request.is_voice_call
        )
        
        # Store conversation
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

@app.post("/voice/process")
async def process_voice(request: VoiceMessage):
    """Process voice input and return text response"""
    try:
        # In a real implementation, you would:
        # 1. Decode the base64 audio data
        # 2. Convert speech to text using Azure Speech Services
        # 3. Process the text with AI brain
        # 4. Return both text and audio response
        
        # For now, return a placeholder response
        return {
            "success": True,
            "text": "Voice processing not fully implemented yet",
            "audio_url": None
        }
    except Exception as e:
        logger.error(f"Voice processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id in conversations:
        return {"conversation": conversations[conversation_id]}
    else:
        return {"conversation": []}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
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
            "real_time_chat": True
        },
        "timestamp": datetime.now(),
        "message": "Cyra AI Assistant with Voice Features"
    }

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "cyra_advanced:app",
        host=settings.host,
        port=8004,  # Use different port
        reload=False,
        log_level=settings.log_level.lower()
    )
