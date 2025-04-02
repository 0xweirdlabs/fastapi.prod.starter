# FastAPI Production Standard Template

A production-ready FastAPI backend template with standardized structure, modularity, and best practices.

## Features

- **Supabase Authentication**: Built-in integration with Supabase Auth and Google OAuth
- **Protected CRUD Example**: Sample CRUD operations protected by authentication
- **Modular Structure**: Well-organized codebase with separation of concerns
- **API Versioning**: Built-in support for API versioning
- **Multiple Database Support**: Easily switch between SQLite, PostgreSQL, and Supabase
- **Resilience Patterns**: Built-in retry and circuit breaker patterns using Stamina
- **Prometheus Monitoring**: Metrics for API, database, and external service calls
- **Environment Separation**: Clear separation between local, dev, and production environments
- **Modern Python Packaging**: Using pyproject.toml for dependency management
- **Docker Integration**: Ready-to-use Docker configurations for different environments

## Quick Start

1. Create a Supabase project and set up Google OAuth
2. Copy `.env.example` to `.env.local` and update with your Supabase credentials
3. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```
4. Run the application:
```bash
python scripts/run.py
```
5. Navigate to `http://localhost:8000/api/v1/auth/login/google` to test authentication

For detailed instructions, see the [Quick Start Guide](./docs/quick-start.md).

## Project Structure

```
fastapi-backend/
├── app/                    # Application code
│   ├── api/                # API routes by version
│   │   └── v1/             # Version 1 API
│   │       ├── routers/    # API endpoint routers
│   │       └── schemas/    # Pydantic models
│   ├── core/               # Core functionality
│   │   ├── auth.py         # Authentication utilities
│   │   └── config.py       # Configuration settings
│   ├── db/                 # Database connections
│   ├── models/             # Database models
│   │   └── item.py         # Example model for CRUD operations
│   └── monitoring/         # Monitoring instrumentation
├── .docker/                # Docker configuration
├── scripts/                # Utility scripts
├── docs/                   # Documentation
├── pyproject.toml          # Project metadata and dependencies
└── .env.example            # Example environment configuration
```

## Authentication

This template uses Supabase for authentication with Google OAuth. It also includes:

- Simplified authentication router for login and callbacks
- User data access through token validation
- Protected endpoints that require authentication

## Protected CRUD Example

The template includes a complete CRUD example for "Items" where:

- All operations require authentication
- Items are associated with the authenticated user
- Users can only access their own items

## Database Configuration

Default configuration uses SQLite for simplicity, but supports PostgreSQL and other databases:

```
# SQLite (Default)
DATABASE_URL=sqlite:///./app.db

# PostgreSQL
DATABASE_URL=postgresql://postgres:password@localhost:5432/yourdb
```

## Running the Application

```bash
# Make sure you're in an activated virtual environment
python scripts/run.py
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Quick Start Guide](./docs/quick-start.md)
- [Testing Documentation](./docs/testing.md)
- [Supabase Setup Guide](./docs/supabase-setup.md)
- [Production Deployment Guide](./docs/production-deployment.md)
- [Security Best Practices](./docs/security-best-practices.md)

## Production Features

The template includes several production-ready features:

- Prometheus metrics for monitoring
- CORS configuration
- Health check endpoint
- Structured logging
- Graceful shutdown

For detailed information about deploying to production, see the [Production Deployment Guide](./docs/production-deployment.md).

## License

MIT
