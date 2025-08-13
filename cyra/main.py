"""
Cyra AI Assistant - Main Entry Point
"""
import asyncio
import logging
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.app import app
from src.core.config import get_settings
import uvicorn

def setup_logging():
    """Configure logging for the application"""
    settings = get_settings()
    
    # Create logs directory if it doesn't exist
    log_file_path = Path(settings.log_file)
    log_file_path.parent.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main function to start Cyra AI Assistant"""
    print("""
    ░█▀▀▀█ █░░█ █▀▀█ █▀▀█ 
    ░█    █▄▄█ █▄▄▀ █▄▄█ 
    ░█▄▄▄█ ▄▄▄█ █▄▄█ █▄▄█ 
    
    🛡️  Cyra AI Assistant v1.0.0
    🤖 Your sophisticated cybersecurity companion
    """)
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        settings = get_settings()
        logger.info("🚀 Starting Cyra AI Assistant...")
        logger.info(f"🌐 Server will be available at: http://{settings.host}:{settings.port}")
        logger.info("📚 API documentation available at: http://localhost:8000/docs")
        
        # Start the server
        uvicorn.run(
            "src.core.app:app",
            host=settings.host,
            port=settings.port,
            reload=settings.debug,
            log_level=settings.log_level.lower(),
            access_log=True
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start Cyra: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
