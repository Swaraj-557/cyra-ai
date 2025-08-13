"""
Authentication module for Cyra AI Assistant
This module handles user authentication, authorization, and session management
"""

# Authentication package for Cyra Enhanced
from .auth_service import AuthService
from .models import UserRegistration, UserLogin, UserProfile, SessionResponse, AuthResponse, PreferencesUpdate

__all__ = ['AuthService', 'UserRegistration', 'UserLogin', 'UserProfile', 'SessionResponse', 'AuthResponse', 'PreferencesUpdate']

# This module is prepared for future implementation of:
# - User registration and login
# - JWT token management
# - Role-based access control
# - Session persistence
# - Password reset functionality
# - Multi-factor authentication

# For now, we use a simple security scheme in the main app
# Future enhancement will implement full user management here
