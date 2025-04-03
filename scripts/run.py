"""
Script to run the FastAPI application directly.
"""
import uvicorn
import signal
import platform
import os
import sys
import atexit

# Updated import paths to reflect the new src structure
from src import app

def load_env_file():
    """Load environment variables from .env.local if it exists"""
    env_file = '.env.local'
    if os.path.exists(env_file):
        print(f"Loading environment from {env_file}")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                os.environ[key] = value
    else:
        print(f"Warning: {env_file} not found. Please create it by copying .env.example")

def register_cleanup():
    """Register a function to clean up resources on exit"""
    def cleanup():
        print("\nShutting down FastAPI server...")
    
    atexit.register(cleanup)
    
    # Handle keyboard interrupts
    def signal_handler(sig, frame):
        print("\nReceived keyboard interrupt. Shutting down...")
        sys.exit(0)
        
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    if platform.system() != "Windows":
        signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    # Register cleanup handlers
    register_cleanup()
    
    # Load environment variables
    load_env_file()
    
    # Print information about how to stop the server
    print("\nFastAPI server starting...")
    print("Press Ctrl+C to stop the server")
    print("Or run 'python scripts/kill.py' from another terminal to stop the server")
    
    # Start the application
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000, reload=True)
