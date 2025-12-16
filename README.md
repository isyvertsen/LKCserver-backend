# Catering System Backend

FastAPI-based backend for the Larvik Kommune Catering Management System.

## Features

- FastAPI with async support
- PostgreSQL database with SQLAlchemy ORM
- JWT authentication with refresh tokens
- Google OAuth integration
- Generic CRUD API for all tables
- Redis for caching and session management
- BDD testing with pytest-bdd
- Docker support

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints (v1 routers)
│   ├── core/         # Core functionality (config, security, migrations)
│   ├── models/       # SQLAlchemy ORM models
│   ├── schemas/      # Pydantic schemas for API validation
│   ├── services/     # Business logic services
│   └── infrastructure/ # Database session management
├── tests/
│   ├── unit/         # Unit tests
│   ├── integration/  # Integration tests
│   └── seed_data.py  # Test database seeding
├── scripts/          # Utility scripts
├── migrations/       # Database migration scripts
└── pyproject.toml    # Dependencies (managed with uv)
```

## Development

### Setup

1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Install dependencies: `uv pip install -r pyproject.toml`
3. Copy `.env.development` and configure database connection
4. Migrations run automatically on server startup

### Running

```bash
# Development server
./start-dev.sh

# Or manually with uv
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# With Docker
docker-compose up backend
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Seed test database
uv run python tests/seed_data.py

# Run E2E tests (from frontend directory)
cd ../frontend
npx playwright test
```

### Database Migrations

**IMPORTANT**: This project uses a custom migration system, NOT Alembic.

- Migrations are defined in `app/core/migrations.py`
- Migrations run automatically on application startup
- Migration status is tracked in the `_migrations` table
- To add a new migration:
  1. Create a new class inheriting from `Migration` in `app/core/migrations.py`
  2. Implement the `up()` method with your migration logic
  3. Register it in the `get_migration_runner()` function
  4. The migration will run automatically on next server start

## API Documentation

When running, API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Environment Variables

See `.env.example` for required environment variables.