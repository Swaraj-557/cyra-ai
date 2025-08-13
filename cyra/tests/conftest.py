"""
Test configuration for Cyra AI Assistant
"""
import pytest
import sys
from pathlib import Path

# Add the project root to Python path for tests
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    from unittest.mock import Mock
    settings = Mock()
    settings.secret_key = "test_secret_key"
    settings.database_url = "sqlite:///:memory:"
    settings.azure_openai_endpoint = "https://test.openai.azure.com/"
    settings.azure_openai_api_key = "test_key"
    settings.azure_openai_deployment_name = "test_deployment"
    settings.azure_speech_key = "test_speech_key"
    settings.azure_speech_region = "test_region"
    return settings

@pytest.fixture
def password_generator():
    """Password generator fixture"""
    from src.tools.password_generator import PasswordGenerator
    return PasswordGenerator()

@pytest.fixture
def tool_manager():
    """Tool manager fixture"""
    from src.tools.tool_manager import ToolManager
    return ToolManager()
