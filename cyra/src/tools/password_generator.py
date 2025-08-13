"""
Password Generator - Secure password generation tool
"""
import secrets
import string
import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PasswordStrength:
    """Password strength assessment result"""
    score: int  # 0-100
    level: str  # Weak, Fair, Good, Strong, Very Strong
    feedback: List[str]
    estimated_crack_time: str


class PasswordGenerator:
    """Secure password generator with strength assessment"""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous_chars = "0O1lI"  # Characters that might be confused
    
    def generate_password(
        self,
        length: int = 16,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_special: bool = True,
        exclude_ambiguous: bool = False,
        custom_charset: Optional[str] = None
    ) -> str:
        """
        Generate a cryptographically secure password
        
        Args:
            length: Password length (minimum 4)
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_special: Include special characters
            exclude_ambiguous: Exclude ambiguous characters
            custom_charset: Use custom character set instead
            
        Returns:
            Generated password string
        """
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        # Build character set
        if custom_charset:
            charset = custom_charset
        else:
            charset = ""
            if include_lowercase:
                charset += self.lowercase
            if include_uppercase:
                charset += self.uppercase
            if include_digits:
                charset += self.digits
            if include_special:
                charset += self.special_chars
        
        if not charset:
            raise ValueError("At least one character type must be included")
        
        # Remove ambiguous characters if requested
        if exclude_ambiguous and not custom_charset:
            for char in self.ambiguous_chars:
                charset = charset.replace(char, "")
        
        # Generate password ensuring at least one character from each selected type
        password = []
        
        # Ensure at least one character from each type is included
        if not custom_charset:
            if include_lowercase:
                password.append(secrets.choice(self.lowercase))
            if include_uppercase:
                password.append(secrets.choice(self.uppercase))
            if include_digits:
                password.append(secrets.choice(self.digits))
            if include_special:
                password.append(secrets.choice(self.special_chars))
        
        # Fill the rest randomly
        remaining_length = length - len(password)
        for _ in range(remaining_length):
            password.append(secrets.choice(charset))
        
        # Shuffle the password to avoid predictable patterns
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def generate_passphrase(
        self,
        word_count: int = 4,
        separator: str = "-",
        include_numbers: bool = True,
        capitalize: bool = True
    ) -> str:
        """
        Generate a memorable passphrase using common words
        
        Args:
            word_count: Number of words to include
            separator: Character to separate words
            include_numbers: Add random numbers
            capitalize: Capitalize first letter of each word
            
        Returns:
            Generated passphrase
        """
        # Common word list (in production, this would be loaded from a file)
        words = [
            "apple", "river", "mountain", "ocean", "forest", "garden", "castle", "bridge",
            "sunset", "melody", "journey", "wisdom", "freedom", "rainbow", "thunder", "crystal",
            "phoenix", "compass", "treasure", "harmony", "mystery", "adventure", "courage", "victory",
            "butterfly", "waterfall", "lighthouse", "telescope", "keyboard", "dinosaur", "elephant", "penguin"
        ]
        
        selected_words = []
        for _ in range(word_count):
            word = secrets.choice(words)
            if capitalize:
                word = word.capitalize()
            selected_words.append(word)
        
        passphrase = separator.join(selected_words)
        
        if include_numbers:
            # Add 2-4 random digits
            num_digits = secrets.randbelow(3) + 2
            random_number = ''.join(secrets.choice(self.digits) for _ in range(num_digits))
            passphrase += separator + random_number
        
        return passphrase
    
    def assess_password_strength(self, password: str) -> PasswordStrength:
        """
        Assess the strength of a given password
        
        Args:
            password: Password to assess
            
        Returns:
            PasswordStrength object with detailed analysis
        """
        score = 0
        feedback = []
        
        # Length scoring
        length = len(password)
        if length >= 12:
            score += 25
        elif length >= 8:
            score += 15
            feedback.append("Consider using a longer password (12+ characters)")
        else:
            score += 5
            feedback.append("Password is too short. Use at least 8 characters, preferably 12+")
        
        # Character variety scoring
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        
        char_types = sum([has_lower, has_upper, has_digit, has_special])
        score += char_types * 10
        
        if not has_lower:
            feedback.append("Add lowercase letters")
        if not has_upper:
            feedback.append("Add uppercase letters")
        if not has_digit:
            feedback.append("Add numbers")
        if not has_special:
            feedback.append("Add special characters (!@#$%^&*)")
        
        # Pattern detection (reduce score for common patterns)
        if re.search(r'(.)\1{2,}', password):  # Repeated characters
            score -= 10
            feedback.append("Avoid repeating characters")
        
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):  # Sequential numbers
            score -= 10
            feedback.append("Avoid sequential numbers")
        
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
            score -= 10
            feedback.append("Avoid sequential letters")
        
        # Common passwords check (simplified)
        common_passwords = [
            'password', '123456', 'password123', 'admin', 'qwerty',
            'letmein', 'welcome', 'monkey', '1234567890'
        ]
        if password.lower() in common_passwords:
            score -= 30
            feedback.append("This is a commonly used password. Choose something unique.")
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        # Determine strength level
        if score >= 80:
            level = "Very Strong"
        elif score >= 60:
            level = "Strong"
        elif score >= 40:
            level = "Good"
        elif score >= 20:
            level = "Fair"
        else:
            level = "Weak"
        
        # Estimate crack time (simplified calculation)
        if score >= 80:
            crack_time = "Centuries to crack"
        elif score >= 60:
            crack_time = "Years to crack"
        elif score >= 40:
            crack_time = "Months to crack"
        elif score >= 20:
            crack_time = "Days to crack"
        else:
            crack_time = "Hours to crack"
        
        if not feedback:
            feedback.append("Excellent password! Keep it secure.")
        
        return PasswordStrength(
            score=score,
            level=level,
            feedback=feedback,
            estimated_crack_time=crack_time
        )
    
    def generate_multiple_passwords(
        self,
        count: int = 5,
        **kwargs
    ) -> List[str]:
        """
        Generate multiple password options
        
        Args:
            count: Number of passwords to generate
            **kwargs: Arguments passed to generate_password()
            
        Returns:
            List of generated passwords
        """
        return [self.generate_password(**kwargs) for _ in range(count)]
    
    def check_breach_patterns(self, password: str) -> List[str]:
        """
        Check for patterns commonly found in breached passwords
        
        Args:
            password: Password to check
            
        Returns:
            List of warnings about potential vulnerabilities
        """
        warnings = []
        
        # Check for keyboard patterns
        keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '1234', '!@#$']
        for pattern in keyboard_patterns:
            if pattern in password.lower():
                warnings.append(f"Contains keyboard pattern: {pattern}")
        
        # Check for common substitutions
        substitutions = {
            '@': 'a', '3': 'e', '1': 'i', '0': 'o', '5': 's', '7': 't'
        }
        simplified = password.lower()
        for char, replacement in substitutions.items():
            simplified = simplified.replace(char, replacement)
        
        common_words = ['password', 'admin', 'user', 'login', 'welcome']
        for word in common_words:
            if word in simplified:
                warnings.append(f"Contains common word: {word}")
        
        return warnings
