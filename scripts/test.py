"""
Test runner script for FastAPI application.
Run with: uv run scripts/test.py [args]
"""
import subprocess
import sys

# Updated import paths to reflect the new src structure
import uv

def main():
    """Run tests with UV"""
    # Install test dependencies
    subprocess.run(["uv", "pip", "install", "-e", ".[dev]"], check=True)
    
    # Build the pytest command
    cmd = ["pytest"]
    
    # Add coverage by default if no specific tests are specified
    if len(sys.argv) <= 1:
        cmd.extend(["--cov=src/app", "--cov-report=term-missing"])
    else:
        # Add any arguments passed to the script
        cmd.extend(sys.argv[1:])
    
    # Run the tests
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
