"""
Simple test of the password generator
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.tools.password_generator import PasswordGenerator
    
    print("🔐 Testing Password Generator...")
    pg = PasswordGenerator()
    
    # Generate a password
    password = pg.generate_password(length=12)
    print(f"Generated password: {password}")
    
    # Check strength
    strength = pg.assess_password_strength(password)
    print(f"Strength: {strength.level} (Score: {strength.score})")
    
    print("✅ Password generator test completed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
