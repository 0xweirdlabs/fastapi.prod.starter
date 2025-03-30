# Installation Guide

This guide will help you install the necessary prerequisites and set up the FastAPI project.

## Prerequisites

- Python 3.10 or newer
- UV package manager (instructions below)
- Docker and Docker Compose (if using containerized environments)

## Installing UV

UV is a modern, fast package manager for Python. Here's how to install it:

### Windows

Using PowerShell:

```powershell
# Install UV using pip
pip install uv

# Verify installation
uv --version
```

### Linux/macOS

```bash
# Install UV using pip
pip install uv

# Verify installation
uv --version
```

## Setting Up the Project

1. Clone or download the project template

2. Create a virtual environment with UV (recommended):

```bash
# Navigate to the project directory
cd fastapi.basic.standard

# Create a virtual environment
uv venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

3. Install the project in development mode:

```bash
# Install the project and its dependencies
uv pip install -e .
```

## Running the Project

### Local Development (without Docker)

1. Copy `.env.example` to `.env.local` and adjust values as needed

2. Activate your virtual environment if not already activated

3. Run the local development server:

```bash
# Using Python directly
python scripts/local.py

# Or if UV is in your PATH
uv run scripts/local.py
```

### Using Docker

1. Copy `.env.example` to `.env.dev` or `.env.prod` depending on your environment

2. Run the appropriate environment:

```bash
# For development
python scripts/dev.py

# For production
python scripts/prod.py
```

## Running Tests

```bash
# Activate your virtual environment if not already activated

# Run all tests
python scripts/test.py

# Run specific tests
python scripts/test.py tests/unit
```
