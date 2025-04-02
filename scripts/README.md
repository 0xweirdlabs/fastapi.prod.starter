# Utility Scripts

This directory contains utility scripts for various project tasks.

## Available Scripts

- `run.py` - Start the FastAPI server with auto-reload and dependency checking
- `kill.py` - Stop the running server
- `dev.py` - Start development environment using Docker Compose
- `prod.py` - Start production environment using Docker Compose
- `test.py` - Run tests using pytest with code coverage
- `migrate_to_supabase.py` - Migrate data from SQLite to Supabase

## Usage

```bash
# Run the application (recommended)
python scripts/run.py

# Stop the application
python scripts/kill.py

# Run tests
python scripts/test.py
```

See the [scripts documentation](../docs/scripts.md) for more details.
