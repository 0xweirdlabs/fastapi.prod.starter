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

# Now run scripts within this activated environment
```

All scripts assume you are running them from an activated virtual environment.

### Starting the Server

```bash
# Start the application with dependency checking and hot-reload
python scripts/run.py
```

This script:
- Installs required dependencies in your current environment if they're missing
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

### Local Development

```bash
# Start local development without Docker
python scripts/local.py
```

This script loads environment variables from `.env.local` and starts the server.

### Development Environment

```bash
# Start development environment with Docker
python scripts/dev.py
```

This script starts the development stack using Docker Compose.

### Production Environment

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

This script migrates user accounts and data from the local SQLite database to Supabase.
