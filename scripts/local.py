"""
Local development script for FastAPI application.
Run with: uv run scripts/local.py
"""
import os
import subprocess
import sys
from src import app

def load_env(env_file):
    """Load environment variables from file"""
    if not os.path.exists(env_file):
        print(f"Environment file {env_file} not found. Please create it by copying .env.example")
        sys.exit(1)
    
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            os.environ[key] = value

def main():
    """Run the local development server"""
    # Load environment variables
    load_env('.env.local')
    
    # Install dependencies
    subprocess.run(["uv", "pip", "install", "-e", "."], check=True)
    
    # Run migrations (uncomment when needed)
    # subprocess.run(["alembic", "upgrade", "head"], check=True)
    
    # Start the development server
    subprocess.run(["uvicorn", "src.app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])

if __name__ == "__main__":
    main()
