# FastAPI Production Standard Template

A production-ready FastAPI backend template with standardized structure, modularity, and best practices.

## Features

- **Modular Structure**: Well-organized codebase with separation of concerns
- **API Versioning**: Built-in support for API versioning
- **Multiple Database Support**: Easily switch between SQLite, PostgreSQL, and Supabase
- **Authentication Options**: 
  - Supabase Auth with Google OAuth
  - Traditional JWT authentication (local fallback)
- **Resilience Patterns**: Built-in retry and circuit breaker patterns using Stamina
- **Prometheus Monitoring**: Metrics for API, database, and external service calls
- **Security**: JWT authentication and password hashing
- **Environment Separation**: Clear separation between local, dev, and production environments
- **Modern Python Packaging**: Using pyproject.toml for dependency management
- **Docker Integration**: Ready-to-use Docker configurations for different environments

## Project Structure

```
fastapi-backend/
├── app/                    # Application code
│   ├── api/                # API routes by version
│   ├── core/               # Core functionality
│   ├── common/             # Shared utilities across versions
│   ├── models/             # Database models
│   ├── db/                 # Database connections
│   ├── repositories/       # Data access layer
│   ├── services/           # Business logic
│   ├── external/           # External API clients
│   └── monitoring/         # Monitoring instrumentation
├── .docker/                # Docker configuration
├── scripts/                # Utility scripts
├── docs/                   # Documentation
├── pyproject.toml          # Project metadata and dependencies
└── .env.example            # Example environment configuration
```

## Getting Started

### Setup

1. Copy `.env.example` to `.env.local`:
```bash
cp .env.example .env.local
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
```bash
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -e .[dev]
```

5. Run the application:
```bash
# Make sure you're in an activated virtual environment
python scripts/run.py
```

6. To stop the server:
```bash
python scripts/kill.py
```

> **Important**: All scripts should be run from within an activated virtual environment. The scripts do not create or activate a virtual environment for you.

For more information about available scripts, see [Scripts Documentation](./docs/scripts.md).

## Authentication Options

The template supports two authentication methods:

### 1. Supabase Authentication with Google OAuth (Preferred)

This template is configured to work with Supabase Auth out of the box. When Supabase is configured, you get:

- Google OAuth authentication
- Session management
- User management in Supabase

#### Supabase Setup Options:

- [Setting up a Supabase Cloud Project](./docs/supabase-setup.md)
- [Setting up a Local Supabase Development Environment](./docs/supabase-local-dev.md)

### 2. Local JWT Authentication (Fallback)

When Supabase is not configured, the template automatically falls back to local JWT authentication:

- Email/password authentication
- JWT token generation and validation
- User data stored in the local database

The fallback authentication still uses the same endpoints, making it easy to transition to Supabase later.

## Database Configuration

This template starts with SQLite by default for simplicity, but supports PostgreSQL and Supabase with minimal changes:

### SQLite (Default)
```
DATABASE_URL=sqlite:///./app.db
```

### PostgreSQL
Uncomment and configure in your .env file:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/yourdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=yourdb
```

### Supabase
Configure in your .env file:
```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
```

## Working with the Template

### Adding a New API Endpoint

1. Create a new router in `app/api/v1/routers/`
2. Add schemas in `app/api/v1/schemas/`
3. Include the router in `app/api/v1/router.py`

### Adding a New Model

1. Create a new model in `app/models/primary/`
2. Create a repository in `app/repositories/`
3. Create a service in `app/services/`

### Adding a New API Version

1. Create a new directory `app/api/v2/`
2. Copy the structure from v1 and modify as needed
3. Include the new router in `app/main.py`

## Testing

Run tests with:

```bash
# Make sure you're in an activated virtual environment
python scripts/test.py
```

For detailed testing specifications, see the [Testing Documentation](./docs/testing.md).

## Docker

### Development Environment

```bash
python scripts/dev.py
```

### Production Environment

```bash
python scripts/prod.py
```

## Production Deployment & Resilience

For production deployments, this template provides comprehensive guidance:

- [Production Deployment Guide](./docs/production-deployment.md) - How to deploy in a horizontally scalable environment
- [Production Resilience Considerations](./docs/production-resilience.md) - Advanced features for building highly resilient systems

## Security

For security best practices, including IP blacklisting strategies at both load balancer and API levels, see the [Security Best Practices](./docs/security-best-practices.md) guide.

## Migrating from SQLite to Supabase

When you're ready to move from local development to Supabase:

1. Set up your Supabase project following one of the Supabase setup guides
2. Run the migration script:

```bash
python scripts/migrate_to_supabase.py
```

## Documentation

- [Testing Documentation](./docs/testing.md)
- [Supabase Setup Guide](./docs/supabase-setup.md)
- [Supabase Local Development](./docs/supabase-local-dev.md)
- [Scripts Documentation](./docs/scripts.md)
- [Production Deployment Guide](./docs/production-deployment.md)
- [Production Resilience Considerations](./docs/production-resilience.md)
- [Security Best Practices](./docs/security-best-practices.md)

## Dependencies

- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- Supabase Python Client
- Stamina (for resilience)
- Prometheus Client (for monitoring)

## License

MIT
