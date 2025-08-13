"""
Cyra Advanced Demo - Showcase all features
"""
import asyncio
import webbrowser
import time
from pathlib import Path

def print_banner():
    print("""
    ░█▀▀▀█ █░░█ █▀▀█ █▀▀█     █▀▀█ █▀▀▄ █░░█ █▀▀█ █▀▀▄ █▀▀ █▀▀ █▀▀▄ 
    ░█    █▄▄█ █▄▄▀ █▄▄█     █▄▄█ █░░█ ░█░█ █▄▄█ █░░█ █░░ █▀▀ █░░█ 
    ░█▄▄▄█ ▄▄▄█ █▄▄█ █▄▄█     ▀░░▀ ▀▀▀░ ░▀▀▀ ▀░░▀ ▀░░▀ ▀▀▀ ▀▀▀ ▀▀▀░ 
    
    🚀 CYRA ADVANCED - ChatGPT-Style Interface with Voice Features
    """)

def showcase_features():
    print("🎯 ADVANCED FEATURES INCLUDED:")
    print()
    
    features = [
        ("🎨 Modern ChatGPT-like Interface", "Dark theme, sidebar, conversation history"),
        ("🎤 Voice Recognition", "Browser-based speech-to-text with Web Speech API"),
        ("🔊 Text-to-Speech", "Natural voice synthesis for responses"),
        ("📞 Live Voice Calls", "Real-time conversation like phone calls"),
        ("💬 Real-time Chat", "WebSocket for instant messaging"),
        ("🔐 Security Tools", "Password generation, analysis, and advice"),
        ("🤖 AI Integration", "GPT-4.1 powered conversations"),
        ("📱 Mobile Responsive", "Works on all devices and screen sizes"),
        ("⚡ Performance", "Fast, modern, and efficient"),
        ("🔄 Auto-Save", "Conversation history and preferences")
    ]
    
    for feature, description in features:
        print(f"   {feature:<35} {description}")
        time.sleep(0.1)
    
    print()

def show_usage_guide():
    print("📋 HOW TO USE CYRA ADVANCED:")
    print()
    
    instructions = [
        "1. 💬 TEXT CHAT",
        "   • Type your questions in the message box",
        "   • Press Enter or click Send",
        "   • Get instant AI-powered responses",
        "",
        "2. 🎤 VOICE RECORDING", 
        "   • Click the 'Record' button",
        "   • Speak your question clearly",
        "   • Click 'Stop' when finished",
        "   • Your speech will be converted to text",
        "",
        "3. 🔊 SPEECH OUTPUT",
        "   • Click 'Speech' to enable voice responses",
        "   • Cyra will speak her answers aloud",
        "   • Toggle on/off as needed",
        "",
        "4. 📞 LIVE CALL MODE",
        "   • Click 'Live Call' for phone-like conversation",
        "   • Speak naturally - no buttons needed",
        "   • Cyra responds with voice automatically",
        "   • Click 'End Call' to stop",
        "",
        "5. 🔐 SECURITY FEATURES",
        "   • Ask: 'Generate a secure password'",
        "   • Ask: 'Check my password strength'", 
        "   • Ask: 'How to protect from phishing?'",
        "   • Get expert cybersecurity advice"
    ]
    
    for instruction in instructions:
        print(f"   {instruction}")
        time.sleep(0.05)
    
    print()

def show_example_commands():
    print("💡 EXAMPLE VOICE COMMANDS:")
    print()
    
    commands = [
        "🔐 'Generate a strong password for my email account'",
        "🛡️ 'How can I protect myself from ransomware?'",
        "📊 'Analyze the strength of my current password'",
        "🌐 'What are the best practices for WiFi security?'",
        "📧 'How do I spot phishing emails?'",
        "🔒 'Should I use two-factor authentication?'",
        "💻 'How to secure my home network?'",
        "📱 'Mobile device security tips'",
        "🏢 'Corporate cybersecurity best practices'",
        "🚨 'What to do if I think I've been hacked?'"
    ]
    
    for cmd in commands:
        print(f"   {cmd}")
        time.sleep(0.1)
    
    print()

def show_browser_requirements():
    print("🌐 BROWSER REQUIREMENTS:")
    print()
    print("   ✅ Chrome (Recommended)")
    print("   ✅ Edge") 
    print("   ✅ Firefox")
    print("   ✅ Safari")
    print()
    print("   📋 Required Features:")
    print("   • Web Speech API (for voice recognition)")
    print("   • Speech Synthesis API (for text-to-speech)")
    print("   • WebSocket support (for real-time chat)")
    print("   • Microphone permissions")
    print()

def main():
    print_banner()
    showcase_features()
    show_usage_guide()
    show_example_commands()
    show_browser_requirements()
    
    print("🚀 READY TO LAUNCH CYRA ADVANCED!")
    print()
    print("📍 Access Points:")
    print("   🌐 Web Interface: http://localhost:8004")
    print("   📖 API Documentation: http://localhost:8004/docs")
    print("   💚 Health Check: http://localhost:8004/health")
    print("   🔌 WebSocket: ws://localhost:8004/ws")
    print()
    
    print("🎯 What makes this special:")
    print("   • ChatGPT-quality interface design")
    print("   • Professional voice interaction")
    print("   • Real-time conversation capabilities")
    print("   • Advanced cybersecurity tools")
    print("   • Production-ready architecture")
    print()
    
    response = input("🚀 Would you like to open Cyra in your browser? (y/n): ").lower().strip()
    
    if response in ['y', 'yes', '']:
        print("🌐 Opening Cyra Advanced in your default browser...")
        try:
            webbrowser.open('http://localhost:8004')
            print("✅ Browser opened successfully!")
            print()
            print("🎤 Don't forget to:")
            print("   1. Allow microphone permissions when prompted")
            print("   2. Try the voice features")
            print("   3. Test the live call mode")
            print("   4. Explore the cybersecurity tools")
            print()
            print("💬 Start by saying: 'Hey Cyra, make me a password!'")
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print("   Please manually navigate to: http://localhost:8004")
    else:
        print("👍 You can access Cyra at: http://localhost:8004")
    
    print("\n🛡️ Enjoy your advanced AI cybersecurity assistant!")

if __name__ == "__main__":
    main()
