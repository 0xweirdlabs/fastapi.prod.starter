# Utility Scripts

This document describes the utility scripts available for managing the application.

## Running the Application

### Virtual Environment Setup (Important!)

The scripts run in your current Python environment. For best practices, always run them inside a virtual environment:

```bash
# Create a virtual environment (if you haven't already)
python -m venv .venv

# Activate the virtual environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# Install dependencies manually
pip install -e .

# Now run scripts within this activated environment
```

All scripts assume you are running them from an activated virtual environment with the required dependencies installed.

### Starting the Server

```bash
# Start the application with hot-reload
python scripts/run.py
```

This script:
- Loads environment variables from `.env.local`
- Starts the FastAPI server with auto-reload enabled
- Sets up signal handling for graceful shutdown

### Stopping the Server

```bash
# Stop the running server
python scripts/kill.py
```

This script:
- Finds the running uvicorn process
- Terminates it gracefully
- Falls back to port-based process termination if needed
- Works on Windows, macOS, and Linux

## Environment Scripts

### Development Environment with Docker

```bash
# Start development environment with Docker
python scripts/dev.py
```

This script starts the development stack using Docker Compose.

### Production Environment with Docker

```bash
# Start production environment with Docker
python scripts/prod.py
```

This script starts the production stack using Docker Compose.

## Testing

```bash
# Run tests with coverage report
python scripts/test.py

# Run specific tests
python scripts/test.py tests/unit
```

This script runs tests using pytest and generates a coverage report.

## Data Migration

```bash
# Migrate data from SQLite to Supabase
python scripts/migrate_to_supabase.py
```

This script migrates data from the local SQLite database to Supabase.

## Script Usage Summary

| Script | Purpose | Command |
|--------|---------|---------|
| `run.py` | Start the application | `python scripts/run.py` |
| `kill.py` | Stop the application | `python scripts/kill.py` |
| `dev.py` | Start Docker development environment | `python scripts/dev.py` |
| `prod.py` | Start Docker production environment | `python scripts/prod.py` |
| `test.py` | Run tests | `python scripts/test.py` |
| `migrate_to_supabase.py` | Migrate data to Supabase | `python scripts/migrate_to_supabase.py` |
