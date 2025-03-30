"""
Production environment script for FastAPI application.
Run with: uv run scripts/prod.py
"""
import subprocess

def main():
    """Run the production environment using Docker"""
    subprocess.run(["docker-compose", "-f", ".docker/docker-compose.prod.yml", "up", "-d"])

if __name__ == "__main__":
    main()
