"""
Icons8 Integration for Cyra Professional
========================================
"""

# Icons8 Premium Icon Mappings
ICONS8_ICONS = {
    # Security Icons (Your 60+ premium icons go here)
    "shield": "/assets/icons/shield.png",
    "lock": "/assets/icons/lock.png", 
    "key": "/assets/icons/key.png",
    "security": "/assets/icons/security.png",
    "firewall": "/assets/icons/firewall.png",
    "encryption": "/assets/icons/encryption.png",
    
    # Interface Icons
    "microphone": "/assets/icons/microphone.png",
    "speaker": "/assets/icons/speaker.png",
    "phone": "/assets/icons/phone.png",
    "chat": "/assets/icons/chat.png",
    "user": "/assets/icons/user.png",
    "settings": "/assets/icons/settings.png",
    
    # Action Icons
    "send": "/assets/icons/send.png",
    "record": "/assets/icons/record.png",
    "stop": "/assets/icons/stop.png",
    "play": "/assets/icons/play.png",
    "pause": "/assets/icons/pause.png",
    "refresh": "/assets/icons/refresh.png",
    
    # Status Icons
    "online": "/assets/icons/online.png",
    "offline": "/assets/icons/offline.png",
    "error": "/assets/icons/error.png",
    "success": "/assets/icons/success.png",
    "warning": "/assets/icons/warning.png",
    "info": "/assets/icons/info.png"
}

def get_icon_url(icon_name: str) -> str:
    """Get URL for Icons8 premium icon"""
    return ICONS8_ICONS.get(icon_name, f"/assets/icons/{icon_name}.png")

def get_fallback_icon(icon_name: str) -> str:
    """Get Font Awesome fallback if Icons8 not available"""
    fallbacks = {
        "shield": "fas fa-shield-alt",
        "lock": "fas fa-lock",
        "microphone": "fas fa-microphone",
        "speaker": "fas fa-volume-up",
        "phone": "fas fa-phone",
        "send": "fas fa-paper-plane",
        "user": "fas fa-user",
        "chat": "fas fa-comments"
    }
    return fallbacks.get(icon_name, "fas fa-circle")
