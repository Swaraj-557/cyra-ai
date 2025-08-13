"""
Simple Web App Launcher for Cyra
"""
import subprocess
import sys
from pathlib import Path
import os

def main():
    print("""
    ░█▀▀▀█ █░░█ █▀▀█ █▀▀█ 
    ░█    █▄▄█ █▄▄▀ █▄▄█ 
    ░█▄▄▄█ ▄▄▄█ █▄▄█ █▄▄█ 
    
    🌐 Cyra Web Application
    🚀 Starting your cybersecurity assistant...
    """)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Set Python path
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd())
    
    print("📍 Server starting at: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "src.core.app:app",
            "--host", "localhost", 
            "--port", "8000",
            "--reload"
        ], env=env)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    main()
