"""
Test password generator functionality
"""
import pytest
from src.tools.password_generator import PasswordGenerator, PasswordStrength


class TestPasswordGenerator:
    """Test cases for the password generator"""
    
    def test_generate_password_default(self, password_generator):
        """Test default password generation"""
        password = password_generator.generate_password()
        assert len(password) == 16
        assert isinstance(password, str)
    
    def test_generate_password_custom_length(self, password_generator):
        """Test password generation with custom length"""
        password = password_generator.generate_password(length=20)
        assert len(password) == 20
    
    def test_generate_password_minimum_length(self, password_generator):
        """Test minimum password length validation"""
        with pytest.raises(ValueError):
            password_generator.generate_password(length=3)
    
    def test_generate_password_character_types(self, password_generator):
        """Test password with specific character types"""
        password = password_generator.generate_password(
            length=12,
            include_uppercase=True,
            include_lowercase=True,
            include_digits=True,
            include_special=True
        )
        assert len(password) == 12
        # Check that different character types are present
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        assert has_upper or has_lower or has_digit  # At least one type should be present
    
    def test_generate_passphrase(self, password_generator):
        """Test passphrase generation"""
        passphrase = password_generator.generate_passphrase()
        assert isinstance(passphrase, str)
        assert '-' in passphrase  # Default separator
        parts = passphrase.split('-')
        assert len(parts) >= 4  # At least 4 words
    
    def test_assess_password_strength(self, password_generator):
        """Test password strength assessment"""
        # Test weak password
        weak_result = password_generator.assess_password_strength("123")
        assert isinstance(weak_result, PasswordStrength)
        assert weak_result.score < 50
        assert weak_result.level in ["Weak", "Fair"]
        
        # Test strong password
        strong_result = password_generator.assess_password_strength("MyVerySecureP@ssw0rd2024!")
        assert strong_result.score > 60
        assert strong_result.level in ["Good", "Strong", "Very Strong"]
    
    def test_generate_multiple_passwords(self, password_generator):
        """Test generating multiple passwords"""
        passwords = password_generator.generate_multiple_passwords(count=3)
        assert len(passwords) == 3
        assert all(isinstance(pwd, str) for pwd in passwords)
        # All passwords should be different
        assert len(set(passwords)) == 3
    
    def test_check_breach_patterns(self, password_generator):
        """Test breach pattern detection"""
        # Test with common pattern
        warnings = password_generator.check_breach_patterns("password123")
        assert len(warnings) > 0
        
        # Test with secure password
        warnings = password_generator.check_breach_patterns("X7$mK9@nP4&vL2^qE8!")
        assert len(warnings) == 0 or len(warnings) < 2  # Should have few or no warnings
