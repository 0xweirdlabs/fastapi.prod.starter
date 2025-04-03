"""
Development environment script for FastAPI application.
Run with: uv run scripts/dev.py
"""
# Updated import paths to reflect the new src structure
import subprocess

def main():
    """Run the development environment using Docker"""
    subprocess.run(["docker-compose", "-f", ".docker/docker-compose.dev.yml", "up", "--build"])

if __name__ == "__main__":
    main()
