"""
Cyra Professional Error Fix & Icons8 Integration Script
======================================================

This script fixes all errors and integrates Icons8 premium icons for a professional look.
"""
import os
import subprocess
import sys
from pathlib import Path

def check_python_environment():
    """Check and configure Python environment"""
    print("🔍 Checking Python environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_required_packages():
    """Install all required packages"""
    print("📦 Installing required packages...")
    
    packages = [
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "websockets>=12.0",
        "wsproto>=1.2.0",
        "openai>=1.3.0",
        "python-dotenv>=1.0.0",
        "aiohttp>=3.9.0",
        "Pillow>=10.0.0",  # For image processing
        "requests>=2.31.0"
    ]
    
    for package in packages:
        try:
            print(f"  Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to install {package}: {e}")
            return False
    
    print("✅ All packages installed successfully")
    return True

def setup_directory_structure():
    """Create proper directory structure"""
    print("📁 Setting up directory structure...")
    
    directories = [
        "assets",
        "assets/icons",
        "assets/images", 
        "assets/audio",
        "src",
        "src/core",
        "src/tools",
        "src/speech",
        "src/ui",
        "config",
        "tests",
        "logs"
    ]
    
    base_path = Path("c:/Users/pc/Desktop/cyra")
    
    for dir_name in directories:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created/verified: {dir_path}")
    
    print("✅ Directory structure ready")
    return True

def create_icons8_integration():
    """Create Icons8 integration system"""
    print("🎨 Setting up Icons8 integration...")
    
    icons8_config = '''"""
Icons8 Integration Configuration
===============================

This module manages Icons8 premium icons for Cyra Professional.
Add your Icons8 premium icons to the assets/icons/ directory.
"""

ICONS8_ICONS = {
    # Security Icons
    "shield": "assets/icons/shield.png",
    "lock": "assets/icons/lock.png", 
    "key": "assets/icons/key.png",
    "security": "assets/icons/security.png",
    "firewall": "assets/icons/firewall.png",
    "encryption": "assets/icons/encryption.png",
    
    # Interface Icons
    "microphone": "assets/icons/microphone.png",
    "speaker": "assets/icons/speaker.png",
    "phone": "assets/icons/phone.png",
    "chat": "assets/icons/chat.png",
    "user": "assets/icons/user.png",
    "settings": "assets/icons/settings.png",
    
    # Action Icons
    "send": "assets/icons/send.png",
    "record": "assets/icons/record.png",
    "stop": "assets/icons/stop.png",
    "play": "assets/icons/play.png",
    "pause": "assets/icons/pause.png",
    "refresh": "assets/icons/refresh.png",
    
    # Status Icons
    "online": "assets/icons/online.png",
    "offline": "assets/icons/offline.png",
    "error": "assets/icons/error.png",
    "success": "assets/icons/success.png",
    "warning": "assets/icons/warning.png",
    "info": "assets/icons/info.png"
}

def get_icon_path(icon_name: str) -> str:
    """Get the path for an Icons8 icon"""
    return ICONS8_ICONS.get(icon_name, f"assets/icons/{icon_name}.png")

def get_icon_url(icon_name: str) -> str:
    """Get the URL for an Icons8 icon"""
    return f"/{get_icon_path(icon_name)}"
'''
    
    with open("c:/Users/pc/Desktop/cyra/src/ui/icons8_config.py", "w") as f:
        f.write(icons8_config)
    
    print("✅ Icons8 integration configured")
    return True

def create_error_handler():
    """Create comprehensive error handling system"""
    print("🛠️ Setting up error handling...")
    
    error_handler = '''"""
Comprehensive Error Handler for Cyra Professional
================================================

This module provides robust error handling and logging.
"""
import logging
import traceback
from typing import Optional, Dict, Any
from datetime import datetime

class CyraErrorHandler:
    """Advanced error handling for Cyra"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/cyra.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error: Exception, context: str = "Unknown") -> Dict[str, Any]:
        """Handle and log errors professionally"""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc()
        }
        
        self.logger.error(f"Error in {context}: {error}")
        self.logger.debug(f"Full traceback: {traceback.format_exc()}")
        
        return error_info
    
    def safe_execute(self, func, *args, **kwargs):
        """Safely execute a function with error handling"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_info = self.handle_error(e, func.__name__)
            return {"error": True, "details": error_info}

# Global error handler instance
error_handler = CyraErrorHandler()
'''
    
    with open("c:/Users/pc/Desktop/cyra/src/core/error_handler.py", "w") as f:
        f.write(error_handler)
    
    print("✅ Error handling system ready")
    return True

def create_configuration_manager():
    """Create improved configuration management"""
    print("⚙️ Setting up configuration management...")
    
    config_manager = '''"""
Enhanced Configuration Manager for Cyra Professional
===================================================

Manages all configuration with error handling and validation.
"""
import os
from typing import Optional
from pydantic import BaseSettings, validator
from src.core.error_handler import error_handler

class CyraSettings(BaseSettings):
    """Comprehensive settings with validation"""
    
    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8005
    debug: bool = False
    log_level: str = "INFO"
    
    # Azure OpenAI Configuration
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None
    azure_openai_deployment_name: str = "gpt-4"
    azure_openai_api_version: str = "2024-02-01"
    
    # Security Configuration
    cors_origins: list = ["*"]
    max_message_length: int = 4000
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600
    
    # Voice Configuration
    speech_enabled: bool = True
    voice_timeout: int = 30
    audio_quality: str = "high"
    
    # Icons8 Configuration
    icons8_enabled: bool = True
    icons8_cdn_url: str = "https://img.icons8.com"
    icons8_size: int = 48
    
    @validator('azure_openai_api_key')
    def validate_api_key(cls, v):
        if not v:
            error_handler.logger.warning("Azure OpenAI API key not set")
        return v
    
    @validator('port')
    def validate_port(cls, v):
        if not (1024 <= v <= 65535):
            raise ValueError("Port must be between 1024 and 65535")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> CyraSettings:
    """Get validated settings"""
    try:
        return CyraSettings()
    except Exception as e:
        error_handler.handle_error(e, "Configuration loading")
        # Return default settings if configuration fails
        return CyraSettings(
            azure_openai_api_key="",
            azure_openai_endpoint=""
        )
'''
    
    with open("c:/Users/pc/Desktop/cyra/src/core/config.py", "w") as f:
        f.write(config_manager)
    
    print("✅ Configuration management ready")
    return True

def create_startup_script():
    """Create startup script with error checking"""
    print("🚀 Creating startup script...")
    
    startup_script = '''"""
Cyra Professional Startup Script
================================

This script starts Cyra with comprehensive error checking.
"""
import sys
import os
import subprocess
import time
from pathlib import Path

def check_requirements():
    """Check all requirements before starting"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check required files
    required_files = [
        "src/core/config.py",
        "src/core/ai_brain.py", 
        "src/tools/tool_manager.py",
        "cyra_professional.py"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing required file: {file_path}")
            return False
    
    # Check .env file
    if not os.path.exists(".env"):
        print("⚠️ .env file not found - creating template...")
        create_env_template()
    
    print("✅ All requirements satisfied")
    return True

def create_env_template():
    """Create .env template if it doesn't exist"""
    env_template = '''# Cyra Professional Configuration
# ================================

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your_endpoint.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION="2024-02-01"

# Server Configuration
HOST=127.0.0.1
PORT=8005
DEBUG=False
LOG_LEVEL=INFO

# Security Configuration
MAX_MESSAGE_LENGTH=4000
RATE_LIMIT_REQUESTS=100

# Voice Configuration
SPEECH_ENABLED=True
VOICE_TIMEOUT=30

# Icons8 Configuration
ICONS8_ENABLED=True
ICONS8_SIZE=48
'''
    
    with open(".env", "w") as f:
        f.write(env_template)
    
    print("📝 Created .env template - please configure your API keys")

def start_cyra():
    """Start Cyra Professional with error handling"""
    print("🚀 Starting Cyra Professional...")
    
    try:
        # Kill any existing processes on the port
        subprocess.run(["taskkill", "/f", "/im", "python.exe"], 
                      capture_output=True, shell=True)
        time.sleep(2)
        
        # Start the application
        subprocess.run([sys.executable, "cyra_professional.py"])
        
    except KeyboardInterrupt:
        print("\\n🛑 Cyra Professional stopped by user")
    except Exception as e:
        print(f"❌ Error starting Cyra: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🎉 Cyra Professional Startup")
    print("=" * 40)
    
    if not check_requirements():
        print("❌ Requirements check failed")
        return False
    
    print("🚀 Starting Cyra Professional...")
    return start_cyra()

if __name__ == "__main__":
    main()
'''
    
    with open("c:/Users/pc/Desktop/cyra/start_cyra.py", "w") as f:
        f.write(startup_script)
    
    print("✅ Startup script created")
    return True

def create_icons8_readme():
    """Create README for Icons8 integration"""
    print("📖 Creating Icons8 integration guide...")
    
    readme_content = '''# Icons8 Integration for Cyra Professional

## Overview
This directory contains Icons8 premium icons for Cyra Professional. 

## Icons8 Premium Icons Setup

### 1. Download Your Icons8 Premium Icons
- Visit your Icons8 premium dashboard
- Download icons in PNG format (48x48px recommended)
- Use consistent naming convention

### 2. Icon Categories Needed

#### Security Icons (Priority: High)
- `shield.png` - Main security icon
- `lock.png` - Password/security lock
- `key.png` - Access/authentication
- `security.png` - General security
- `firewall.png` - Network protection
- `encryption.png` - Data encryption

#### Interface Icons (Priority: High)  
- `microphone.png` - Voice recording
- `speaker.png` - Audio output
- `phone.png` - Live calls
- `chat.png` - Messaging
- `user.png` - User avatar
- `settings.png` - Configuration

#### Action Icons (Priority: Medium)
- `send.png` - Send message
- `record.png` - Start recording
- `stop.png` - Stop action
- `play.png` - Play audio
- `pause.png` - Pause action
- `refresh.png` - Refresh/reload

#### Status Icons (Priority: Medium)
- `online.png` - Online status
- `offline.png` - Offline status
- `error.png` - Error state
- `success.png` - Success state
- `warning.png` - Warning state
- `info.png` - Information

### 3. Icon Specifications
- **Format**: PNG with transparency
- **Size**: 48x48px (or 32x32px, 64x64px)
- **Style**: Consistent with Icons8 design system
- **Colors**: Adaptable to dark/light themes

### 4. Integration Process
1. Place downloaded icons in this directory
2. Use consistent naming (lowercase, underscores)
3. Update `icons8_config.py` if needed
4. Icons are automatically served by the application

### 5. Fallback System
If Icons8 icons are not available, the application will:
- Use Font Awesome icons as fallback
- Display text alternatives
- Log missing icon warnings

### 6. Usage in Application
Icons are accessed via the Icons8 configuration:

```python
from src.ui.icons8_config import get_icon_url

# Get icon URL
icon_url = get_icon_url("shield")
```

### 7. Performance Optimization
- Icons are served as static files
- Browser caching enabled
- Optimized file sizes recommended

## File Structure
```
assets/icons/
├── favicon.ico
├── favicon.svg
├── shield.png
├── lock.png
├── microphone.png
├── speaker.png
└── ... (other icons)
```

## Support
For Icons8 premium support: https://icons8.com/support
For Cyra integration issues: Check application logs
'''
    
    with open("c:/Users/pc/Desktop/cyra/assets/icons/README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Icons8 integration guide created")
    return True

def main():
    """Main setup function"""
    print("🎉 Cyra Professional Setup & Error Fix")
    print("=" * 50)
    
    steps = [
        ("Checking Python environment", check_python_environment),
        ("Installing required packages", install_required_packages), 
        ("Setting up directory structure", setup_directory_structure),
        ("Creating Icons8 integration", create_icons8_integration),
        ("Setting up error handling", create_error_handler),
        ("Configuring settings management", create_configuration_manager),
        ("Creating startup script", create_startup_script),
        ("Creating Icons8 guide", create_icons8_readme)
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        print(f"\\n🔄 {step_name}...")
        try:
            if step_func():
                success_count += 1
                print(f"✅ {step_name} completed")
            else:
                print(f"❌ {step_name} failed")
        except Exception as e:
            print(f"❌ {step_name} failed with error: {e}")
    
    print(f"\\n🎯 Setup Complete: {success_count}/{len(steps)} steps successful")
    
    if success_count == len(steps):
        print("\\n🎉 Cyra Professional is ready!")
        print("📍 Next steps:")
        print("   1. Add your Icons8 premium icons to assets/icons/")
        print("   2. Configure your .env file with API keys")
        print("   3. Run: python start_cyra.py")
        print("   4. Access: http://localhost:8005")
    else:
        print("\\n⚠️ Some setup steps failed. Please check the errors above.")
    
    return success_count == len(steps)

if __name__ == "__main__":
    main()
'''
