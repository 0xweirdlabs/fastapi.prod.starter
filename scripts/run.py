"""
Simple script to run the FastAPI application directly.
This will ensure dependencies are installed before starting the server.
"""
import subprocess
import sys
import uvicorn
import signal
import platform
import os
import atexit

def ensure_dependencies():
    """Ensure all required dependencies are installed"""
    print("Checking dependencies...")
    try:
        # Install the package and its dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Please run: pip install -e .")
        sys.exit(1)

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
    
    # Make sure dependencies are installed
    ensure_dependencies()
    
    # Print information about how to stop the server
    print("\nFastAPI server starting...")
    print("Press Ctrl+C to stop the server")
    print("Or run 'python kill.py' from another terminal to stop the server")
    
    # Start the application
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
