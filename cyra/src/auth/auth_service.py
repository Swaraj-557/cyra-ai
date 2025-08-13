"""
Authentication Service for Cyra Enhanced
========================================

Professional login and registration system with secure password handling
"""
import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.users_file = "data/users.json"
        self.sessions_file = "data/sessions.json"
        self.ensure_data_directory()
        self.load_users()
        self.load_sessions()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def load_users(self):
        """Load users from file"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
            logger.info(f"✅ Loaded {len(self.users)} users")
        except Exception as e:
            logger.error(f"❌ Error loading users: {e}")
            self.users = {}
    
    def save_users(self):
        """Save users to file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
            logger.info("✅ Users saved successfully")
        except Exception as e:
            logger.error(f"❌ Error saving users: {e}")
    
    def load_sessions(self):
        """Load active sessions"""
        try:
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r') as f:
                    self.sessions = json.load(f)
            else:
                self.sessions = {}
            logger.info(f"✅ Loaded {len(self.sessions)} active sessions")
        except Exception as e:
            logger.error(f"❌ Error loading sessions: {e}")
            self.sessions = {}
    
    def save_sessions(self):
        """Save sessions to file"""
        try:
            with open(self.sessions_file, 'w') as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Error saving sessions: {e}")
    
    def hash_password(self, password: str, salt: str = None) -> tuple:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return password_hash.hex(), salt
    
    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verify password against stored hash"""
        password_hash, _ = self.hash_password(password, salt)
        return password_hash == stored_hash
    
    def generate_session_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def register_user(self, username: str, email: str, password: str, full_name: str = "") -> Dict[str, Any]:
        """Register a new user"""
        try:
            # Validate input
            if not username or not email or not password:
                return {"success": False, "message": "All fields are required"}
            
            if len(username) < 3:
                return {"success": False, "message": "Username must be at least 3 characters"}
            
            if len(password) < 6:
                return {"success": False, "message": "Password must be at least 6 characters"}
            
            if "@" not in email:
                return {"success": False, "message": "Invalid email format"}
            
            # Check if user already exists
            if username.lower() in [u.lower() for u in self.users.keys()]:
                return {"success": False, "message": "Username already exists"}
            
            if any(user.get("email", "").lower() == email.lower() for user in self.users.values()):
                return {"success": False, "message": "Email already registered"}
            
            # Hash password
            password_hash, salt = self.hash_password(password)
            
            # Create user record
            user_data = {
                "username": username,
                "email": email,
                "full_name": full_name,
                "password_hash": password_hash,
                "salt": salt,
                "created_at": datetime.now().isoformat(),
                "last_login": None,
                "is_active": True,
                "preferences": {
                    "theme": "dark",
                    "voice_enabled": True,
                    "notifications": True
                }
            }
            
            self.users[username] = user_data
            self.save_users()
            
            logger.info(f"✅ User {username} registered successfully")
            return {
                "success": True,
                "message": "Registration successful! You can now log in.",
                "username": username
            }
            
        except Exception as e:
            logger.error(f"❌ Registration error: {e}")
            return {"success": False, "message": "Registration failed. Please try again."}
    
    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user and create session"""
        try:
            # Find user (case-insensitive)
            user_key = None
            for key in self.users.keys():
                if key.lower() == username.lower():
                    user_key = key
                    break
            
            if not user_key:
                return {"success": False, "message": "Invalid username or password"}
            
            user = self.users[user_key]
            
            # Check if user is active
            if not user.get("is_active", True):
                return {"success": False, "message": "Account is disabled"}
            
            # Verify password
            if not self.verify_password(password, user["password_hash"], user["salt"]):
                return {"success": False, "message": "Invalid username or password"}
            
            # Create session
            session_token = self.generate_session_token()
            session_data = {
                "username": user_key,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(days=7)).isoformat(),
                "ip_address": "localhost",  # Would be actual IP in production
                "user_agent": "Cyra Enhanced"
            }
            
            self.sessions[session_token] = session_data
            self.save_sessions()
            
            # Update last login
            self.users[user_key]["last_login"] = datetime.now().isoformat()
            self.save_users()
            
            logger.info(f"✅ User {username} logged in successfully")
            return {
                "success": True,
                "message": "Login successful!",
                "session_token": session_token,
                "user": {
                    "username": user["username"],
                    "email": user["email"],
                    "full_name": user.get("full_name", ""),
                    "preferences": user.get("preferences", {})
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Login error: {e}")
            return {"success": False, "message": "Login failed. Please try again."}
    
    def verify_session(self, session_token: str) -> Dict[str, Any]:
        """Verify if session is valid"""
        try:
            if not session_token or session_token not in self.sessions:
                return {"valid": False, "message": "Invalid session"}
            
            session = self.sessions[session_token]
            expires_at = datetime.fromisoformat(session["expires_at"])
            
            if datetime.now() > expires_at:
                # Session expired
                del self.sessions[session_token]
                self.save_sessions()
                return {"valid": False, "message": "Session expired"}
            
            username = session["username"]
            if username not in self.users:
                return {"valid": False, "message": "User not found"}
            
            user = self.users[username]
            return {
                "valid": True,
                "user": {
                    "username": user["username"],
                    "email": user["email"],
                    "full_name": user.get("full_name", ""),
                    "preferences": user.get("preferences", {})
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Session verification error: {e}")
            return {"valid": False, "message": "Session verification failed"}
    
    def logout_user(self, session_token: str) -> Dict[str, Any]:
        """Logout user and invalidate session"""
        try:
            if session_token in self.sessions:
                username = self.sessions[session_token]["username"]
                del self.sessions[session_token]
                self.save_sessions()
                logger.info(f"✅ User {username} logged out")
                return {"success": True, "message": "Logged out successfully"}
            else:
                return {"success": False, "message": "Invalid session"}
        except Exception as e:
            logger.error(f"❌ Logout error: {e}")
            return {"success": False, "message": "Logout failed"}
    
    def update_user_preferences(self, username: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Update user preferences"""
        try:
            if username not in self.users:
                return {"success": False, "message": "User not found"}
            
            self.users[username]["preferences"].update(preferences)
            self.save_users()
            
            return {"success": True, "message": "Preferences updated"}
        except Exception as e:
            logger.error(f"❌ Error updating preferences: {e}")
            return {"success": False, "message": "Failed to update preferences"}
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            total_users = len(self.users)
            active_sessions = len(self.sessions)
            
            # Count users by registration date
            today = datetime.now().date()
            users_today = sum(1 for user in self.users.values() 
                            if datetime.fromisoformat(user["created_at"]).date() == today)
            
            return {
                "total_users": total_users,
                "active_sessions": active_sessions,
                "new_users_today": users_today,
                "success": True
            }
        except Exception as e:
            logger.error(f"❌ Error getting user stats: {e}")
            return {"success": False, "message": "Failed to get statistics"}
